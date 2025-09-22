"use client";

import { useState, useCallback, useRef, useEffect } from "react";
import { Message } from "@/components/chat";

export interface UseChatOptions {
  initialMessages?: Message[];
  onResponse?: (message: Message) => void;
  onError?: (error: Error) => void;
  api?: string;
  maxRetries?: number;
  saveChatHistory?: boolean;
}

export interface UseChatReturn {
  messages: Message[];
  isLoading: boolean;
  error: Error | null;
  sendMessage: (content: string) => Promise<void>;
  clearMessages: () => void;
  regenerateResponse: (messageId: string) => Promise<void>;
  stopGeneration: () => void;
  retry: () => Promise<void>;
}

export function useChat(options: UseChatOptions = {}): UseChatReturn {
  const {
    initialMessages = [],
    onResponse,
    onError,
    api = "/api/chat",
    maxRetries = 3,
  } = options;

  // Initialize messages with validated initialMessages using useState initializer
  const [messages, setMessages] = useState<Message[]>(() => {
    // Ensure initialMessages are valid before setting state
    if (Array.isArray(initialMessages) && initialMessages.length > 0) {
      // Make sure each message has the required properties
      return initialMessages.map((msg) => ({
        id:
          msg.id ||
          `msg-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`,
        message: msg.message || "",
        type: msg.type || "system",
        timestamp: msg.timestamp instanceof Date ? msg.timestamp : new Date(),
      }));
    }
    return [];
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);
  const [retryCount, setRetryCount] = useState(0);
  const abortControllerRef = useRef<AbortController | null>(null);
  const lastUserMessageRef = useRef<string>("");

  const stopGeneration = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    setIsLoading(false);
  }, []);

  const sendMessage = useCallback(
    async (content: string) => {
      if (isLoading) return;

      lastUserMessageRef.current = content;
      setError(null);
      setIsLoading(true);

      // Add user message
      const userMessage: Message = {
        id: `user-${Date.now()}`,
        message: content,
        type: "user",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, userMessage]);

      try {
        // Create abort controller
        abortControllerRef.current = new AbortController();

        // We don't need to modify the API endpoint here anymore - that should be handled
        // by the ClientWrapper component that correctly formats the API endpoint
        const apiEndpoint = api;

        // Prepare request body based on whether it's a new chat or existing chat
        const requestBody = {
          message: content,
        };

        // Call API
        const response = await fetch(apiEndpoint, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestBody),
          signal: abortControllerRef.current.signal,
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Handle streaming response
        const reader = response.body?.getReader();
        const decoder = new TextDecoder();
        let assistantContent = "";

        const assistantMessage: Message = {
          id: `assistant-${Date.now()}`,
          message: "",
          type: "ai",
          timestamp: new Date(),
        };

        // Add empty assistant message
        setMessages((prev) => [...prev, assistantMessage]);

        if (reader) {
          try {
            while (true) {
              const { done, value } = await reader.read();
              if (done) break;

              // Decode the chunk
              const chunk = decoder.decode(value, { stream: true });

              // Append to our content
              assistantContent += chunk;

              // Update the message immediately
              setMessages((prev) => {
                const newMessages = [...prev];
                const lastIndex = newMessages.length - 1;
                if (lastIndex >= 0 && newMessages[lastIndex].type === "ai") {
                  newMessages[lastIndex] = {
                    ...newMessages[lastIndex],
                    message: assistantContent,
                  };
                }
                return newMessages;
              });
            }
          } catch (streamError) {
            // Silent error handling for stream reading
            console.error("Stream reading error:", streamError);
          }
        }

        // Final assistant message
        const finalMessage: Message = {
          ...assistantMessage,
          message:
            assistantContent ||
            "Sorry, I encountered an error generating a response.",
        };

        setMessages((prev) => {
          const newMessages = [...prev];
          newMessages[newMessages.length - 1] = finalMessage;
          return newMessages;
        });

        onResponse?.(finalMessage);
        setRetryCount(0);
      } catch (err) {
        if (err instanceof Error && err.name === "AbortError") {
          // Request was aborted
          setMessages((prev) => prev.slice(0, -1)); // Remove the empty assistant message
          return;
        }

        const error =
          err instanceof Error ? err : new Error("Unknown error occurred");
        setError(error);
        onError?.(error);

        // Remove the empty assistant message on error
        setMessages((prev) => prev.slice(0, -1));
      } finally {
        setIsLoading(false);
        abortControllerRef.current = null;
      }
    },
    [isLoading, api, onResponse, onError]
  );

  const clearMessages = useCallback(() => {
    setMessages([]);
    setError(null);
    setRetryCount(0);
  }, []);

  const regenerateResponse = useCallback(
    async (messageId: string) => {
      const messageIndex = messages.findIndex((msg) => msg.id === messageId);
      if (messageIndex === -1) return;

      const previousUserMessage = messages[messageIndex - 1];
      if (!previousUserMessage || previousUserMessage.type !== "user") return;

      // Remove the message we're regenerating
      setMessages((prev) => prev.slice(0, messageIndex));

      // Resend the previous user message
      await sendMessage(previousUserMessage.message);
    },
    [messages, sendMessage]
  );

  const retry = useCallback(async () => {
    if (retryCount >= maxRetries) {
      setError(new Error(`Max retries (${maxRetries}) exceeded`));
      return;
    }

    setRetryCount((prev) => prev + 1);
    await sendMessage(lastUserMessageRef.current);
  }, [retryCount, maxRetries, sendMessage]);

  return {
    messages,
    isLoading,
    error,
    sendMessage,
    clearMessages,
    regenerateResponse,
    stopGeneration,
    retry,
  };
}
