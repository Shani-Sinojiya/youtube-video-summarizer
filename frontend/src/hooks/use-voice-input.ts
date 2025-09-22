import { useState, useRef, useCallback, useEffect } from "react";

interface SpeechRecognitionEvent extends Event {
  results: SpeechRecognitionResultList;
  resultIndex: number;
}

interface SpeechRecognitionErrorEvent extends Event {
  error: string;
  message: string;
}

interface SpeechRecognition extends EventTarget {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  start(): void;
  stop(): void;
  abort(): void;
  onstart: ((this: SpeechRecognition, ev: Event) => void) | null;
  onend: ((this: SpeechRecognition, ev: Event) => void) | null;
  onresult:
    | ((this: SpeechRecognition, ev: SpeechRecognitionEvent) => void)
    | null;
  onerror:
    | ((this: SpeechRecognition, ev: SpeechRecognitionErrorEvent) => void)
    | null;
}

declare global {
  interface Window {
    SpeechRecognition: {
      new (): SpeechRecognition;
    };
    webkitSpeechRecognition: {
      new (): SpeechRecognition;
    };
  }
}

export interface UseVoiceInputReturn {
  isListening: boolean;
  isSupported: boolean;
  transcript: string;
  interimTranscript: string;
  error: string | null;
  startListening: () => void;
  stopListening: () => void;
  resetTranscript: () => void;
  retryVoiceInput: () => void;
}

export function useVoiceInput(): UseVoiceInputReturn {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState("");
  const [interimTranscript, setInterimTranscript] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSupported, setIsSupported] = useState(false);
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const reconnectAttemptsRef = useRef(0);
  const maxReconnectAttempts = 3;

  // Check for browser support on client-side only
  useEffect(() => {
    if (typeof window !== "undefined") {
      const hasSpeechRecognition =
        "SpeechRecognition" in window || "webkitSpeechRecognition" in window;

      if (hasSpeechRecognition) {
        try {
          const SpeechRecognition =
            window.SpeechRecognition || window.webkitSpeechRecognition;
          const testRecognition = new SpeechRecognition();
          testRecognition.abort();
          setIsSupported(true);
        } catch (err) {
          console.error("Speech recognition test failed:", err);
          setIsSupported(false);
        }
      } else {
        setIsSupported(false);
      }
    }
  }, []);

  // Helper function to format transcript text - memoized to prevent infinite loops
  const formatTranscript = useCallback(
    (text: string, currentTranscript: string): string => {
      if (!text) return "";

      // Add space if needed for concatenation
      const needsLeadingSpace =
        text.charAt(0) !== " " &&
        text.charAt(0) !== "." &&
        text.charAt(0) !== "," &&
        text.charAt(0) !== "?" &&
        text.charAt(0) !== "!";

      // Capitalize first letter if it starts a new sentence
      // (after period, question mark, exclamation mark, or is the first transcript)
      const shouldCapitalize =
        !currentTranscript ||
        currentTranscript.endsWith(".") ||
        currentTranscript.endsWith("?") ||
        currentTranscript.endsWith("!");

      let formattedText = text;

      if (shouldCapitalize && formattedText.length > 0) {
        formattedText =
          formattedText.charAt(0).toUpperCase() + formattedText.slice(1);
      }

      // Add leading space if needed and not at the start of a message
      return (
        (currentTranscript && needsLeadingSpace ? " " : "") + formattedText
      );
    },
    []
  );

  const checkNetworkConnectivity = useCallback(() => {
    return typeof navigator !== "undefined" && navigator.onLine;
  }, []);

  // Process recognition results
  const processRecognitionResult = useCallback(
    (event: SpeechRecognitionEvent) => {
      let finalTranscript = "";
      let currentInterimTranscript = "";

      // Process all results
      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i];
        const transcript = result[0].transcript;

        if (result.isFinal) {
          finalTranscript += transcript;
        } else {
          currentInterimTranscript += transcript;
        }
      }

      // Apply formatting and update state
      if (finalTranscript) {
        setInterimTranscript("");
        setTranscript((prevTranscript) => {
          const formattedText = formatTranscript(
            finalTranscript,
            prevTranscript
          );
          if (prevTranscript.endsWith(formattedText)) {
            return prevTranscript;
          }
          return prevTranscript + formattedText;
        });
      } else if (currentInterimTranscript) {
        setInterimTranscript(currentInterimTranscript);
      }
    },
    [formatTranscript]
  );

  const startListening = useCallback(() => {
    if (!isSupported) {
      setError("Speech recognition is not supported in this browser");
      return;
    }

    if (!checkNetworkConnectivity()) {
      setError(
        "Network connection is offline. Please check your internet connection and try again."
      );
      return;
    }

    if (isListening) return;

    // Reset error state when starting
    setError(null);

    try {
      // Force cleanup of any existing recognition instance
      if (recognitionRef.current) {
        try {
          recognitionRef.current.abort();
          recognitionRef.current = null;
        } catch (e) {
          console.error("Error cleaning up previous recognition:", e);
        }
      }

      // Create a new speech recognition instance
      const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRecognition) {
        setError("Speech recognition is not supported in this browser");
        return;
      }

      const recognition = new SpeechRecognition();

      // Configure recognition instance
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = "en-US";

      // Set a timeout to detect if recognition doesn't start properly
      const startTimeout = setTimeout(() => {
        if (recognitionRef.current && isListening) {
          recognition.stop();
          setError("Speech recognition failed to start. Please try again.");
        }
      }, 3000);

      recognition.onstart = () => {
        clearTimeout(startTimeout);
        setIsListening(true);
        setError(null);
        setInterimTranscript("");
        reconnectAttemptsRef.current = 0;
      };

      recognition.onresult = (event: SpeechRecognitionEvent) => {
        processRecognitionResult(event);
      };

      recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
        let errorMessage = "Speech recognition error";
        let shouldReconnect = false;

        // Before handling error, save any current interim transcript
        if (interimTranscript && interimTranscript.trim()) {
          setTranscript(
            (prev) => prev + formatTranscript(interimTranscript, prev)
          );
          setInterimTranscript("");
        }

        // Provide more user-friendly error messages
        switch (event.error) {
          case "not-allowed":
            errorMessage =
              "Microphone access denied. Please allow microphone access.";
            break;
          case "network":
            errorMessage = "Network error. Please check your connection.";
            shouldReconnect = true;
            break;
          case "service-not-allowed":
            errorMessage =
              "Speech service not available. Please try again later.";
            shouldReconnect = true;
            break;
          case "no-speech":
            errorMessage = "No speech detected. Please try again.";
            break;
          case "aborted":
            errorMessage = "Voice input was aborted.";
            break;
          default:
            errorMessage = `Speech recognition error: ${event.error}`;
            // For unknown errors, try to reconnect
            shouldReconnect = true;
        }

        // Check if browser is online before showing network error
        if (shouldReconnect && !checkNetworkConnectivity()) {
          errorMessage =
            "Your device appears to be offline. Please check your internet connection.";
          shouldReconnect = false; // Don't try to reconnect if definitely offline
        }

        setError(errorMessage);

        // Try to reconnect for network errors
        if (
          shouldReconnect &&
          reconnectAttemptsRef.current < maxReconnectAttempts
        ) {
          reconnectAttemptsRef.current += 1;
          setError(
            `${errorMessage} Attempting to reconnect... (${reconnectAttemptsRef.current}/${maxReconnectAttempts})`
          );

          // Stop current recognition
          if (recognitionRef.current) {
            recognitionRef.current.onend = null; // Prevent onend from firing during reconnect
            recognitionRef.current.abort();
          }

          // Try to reconnect after a short delay
          setTimeout(() => {
            if (checkNetworkConnectivity()) {
              startListening();
            } else {
              setError(
                "Still offline. Please check your internet connection and try again."
              );
              setIsListening(false);
            }
          }, 1500);
        } else if (shouldReconnect) {
          // Max reconnect attempts reached
          setError(
            `${errorMessage} Reconnection failed after ${maxReconnectAttempts} attempts.`
          );
          setIsListening(false);
        } else {
          // Not a reconnectable error
          setIsListening(false);
        }
      };

      recognition.onend = () => {
        // Check if this is a manual stop (via stopListening) and skip processing if so
        if (recognitionRef.current === null) {
          return; // This was a manual stop, skip onend processing
        }

        // If we're trying to reconnect, don't process the end event
        if (
          reconnectAttemptsRef.current > 0 &&
          reconnectAttemptsRef.current < maxReconnectAttempts
        ) {
          return;
        }

        // Push any remaining interim transcript as final when recognition ends
        if (interimTranscript) {
          setTranscript(interimTranscript);
          setInterimTranscript("");
        }

        setIsListening(false);

        // Check for abrupt disconnection without error
        if (isListening && !error && checkNetworkConnectivity()) {
          // Recognition ended unexpectedly, could be a silent failure
          // Only show this if we're not already showing an error
          setError("Voice recognition stopped unexpectedly. Please try again.");
        }
      };

      // Schedule periodic checks for network issues during listening
      let networkCheckInterval: NodeJS.Timeout | null = null;

      if (checkNetworkConnectivity()) {
        networkCheckInterval = setInterval(() => {
          if (!checkNetworkConnectivity() && isListening) {
            setError(
              "Network connection lost. Voice recognition will resume when your connection is restored."
            );

            // Stop current recognition but don't set isListening to false yet
            if (recognitionRef.current) {
              try {
                recognitionRef.current.abort();
              } catch (err) {
                console.error(
                  "Error aborting recognition during network loss:",
                  err
                );
              }
            }

            // Set up a listener for when connection is restored
            const checkConnectionAndRestart = () => {
              if (checkNetworkConnectivity()) {
                // Connection restored, try to restart
                window.removeEventListener("online", checkConnectionAndRestart);
                startListening();
              }
            };

            window.addEventListener("online", checkConnectionAndRestart);
          }
        }, 2000);
      }

      recognitionRef.current = recognition;
      recognition.start();

      return () => {
        if (networkCheckInterval) {
          clearInterval(networkCheckInterval);
        }
      };
    } catch (err) {
      console.error("Failed to start speech recognition:", err);
      setError("Failed to start speech recognition");
      setIsListening(false);
    }
  }, [
    isSupported,
    isListening,
    checkNetworkConnectivity,
    processRecognitionResult,
    formatTranscript,
    interimTranscript,
    error,
  ]);

  const stopListening = useCallback(() => {
    // Clear any pending network check intervals
    if (typeof window !== "undefined") {
      const win = window as Window & {
        _voiceNetworkCheckInterval?: NodeJS.Timeout;
      };
      if (win._voiceNetworkCheckInterval) {
        clearInterval(win._voiceNetworkCheckInterval);
        win._voiceNetworkCheckInterval = undefined;
      }
    }

    // Reset reconnect attempts on manual stop
    reconnectAttemptsRef.current = 0;

    // Store the current interim transcript value BEFORE any state changes
    const currentInterimText = interimTranscript;

    // Process the interim transcript BEFORE stopping the recognition
    if (currentInterimText && currentInterimText.trim()) {
      try {
        setTranscript((prevTranscript) => {
          const formattedText = formatTranscript(
            currentInterimText,
            prevTranscript
          );
          return prevTranscript + formattedText;
        });
        setInterimTranscript("");
      } catch (err) {
        console.error("Error updating transcript:", err);
      }
    }

    // Set listening state to false for UI responsiveness
    setIsListening(false);

    // Then try to gracefully stop the recognition
    if (recognitionRef.current) {
      try {
        // Detach all event handlers to prevent callbacks during shutdown
        recognitionRef.current.onend = null;
        recognitionRef.current.onerror = null;
        recognitionRef.current.onresult = null;
        recognitionRef.current.onstart = null;

        // Try abort first as it's more reliable at stopping immediately
        recognitionRef.current.abort();

        // Also try the regular stop method as a fallback
        try {
          recognitionRef.current.stop();
        } catch (innerErr) {
          console.error("Error during stop fallback:", innerErr);
        }

        // Clear the recognition reference
        recognitionRef.current = null;
      } catch (err) {
        console.error("Error stopping recognition:", err);
        recognitionRef.current = null;
      }
    }
  }, [interimTranscript, formatTranscript]);

  // Add network status monitoring
  useEffect(() => {
    const handleOnline = () => {
      if (error && error.includes("offline") && !isListening) {
        setError("Network connection restored. Try voice input again.");
      }
    };

    const handleOffline = () => {
      if (isListening) {
        setError(
          "Network connection lost. Please check your internet connection."
        );
        if (recognitionRef.current) {
          recognitionRef.current.abort();
        }
        setIsListening(false);
      }
    };

    window.addEventListener("online", handleOnline);
    window.addEventListener("offline", handleOffline);

    return () => {
      window.removeEventListener("online", handleOnline);
      window.removeEventListener("offline", handleOffline);
    };
  }, [isListening, error]);

  const resetTranscript = useCallback(() => {
    setTranscript("");
    setInterimTranscript("");
    setError(null);
  }, []);

  // Add a dedicated retry function for better UX
  const retryVoiceInput = useCallback(() => {
    // First check if network is available
    if (!checkNetworkConnectivity()) {
      setError(
        "Still offline. Please check your internet connection before retrying."
      );
      return;
    }

    // Reset errors and reconnection attempts
    setError(null);
    reconnectAttemptsRef.current = 0;

    // Force cleanup of any existing recognition
    if (recognitionRef.current) {
      try {
        recognitionRef.current.abort();
      } catch (err) {
        console.error("Error during cleanup:", err);
      }
      recognitionRef.current = null;
    }

    // Small delay before retry to allow browser to properly release resources
    setTimeout(() => {
      startListening();
    }, 300);
  }, [checkNetworkConnectivity, startListening]);

  return {
    isListening,
    isSupported,
    transcript,
    interimTranscript,
    error,
    startListening,
    stopListening,
    resetTranscript,
    retryVoiceInput,
  };
}
