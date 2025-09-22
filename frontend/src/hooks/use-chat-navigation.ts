"use client";

import { useRouter, useParams } from "next/navigation";
import { v7 as uuidv7 } from "uuid";
import { useCallback } from "react";

// This is a simple way to pass the initial message when navigating
// In a production app, you might use a more robust state management solution
const pendingMessages: Record<string, string> = {};

export function useChatNavigation() {
  const router = useRouter();
  const params = useParams();
  const currentChatId = params?.id as string;

  const navigateToNewChat = useCallback(
    (content: string) => {
      // Only create a new chat ID if we're on the /chat/new route
      if (currentChatId === "new") {
        // Generate a new UUID for the session
        const newChatId = uuidv7();

        // Store the message to be sent after navigation
        pendingMessages[newChatId] = content;

        // Navigate to the new chat
        router.push(`/chat/${newChatId}`);
        return true; // Indicate that navigation occurred
      }
      return false; // No navigation occurred
    },
    [currentChatId, router]
  );

  // Check if there's a pending message for this chat ID
  const getPendingMessage = useCallback(() => {
    if (currentChatId && currentChatId !== "new") {
      const message = pendingMessages[currentChatId];
      // Clear the message after retrieving it
      if (message) {
        delete pendingMessages[currentChatId];
      }
      return message;
    }
    return null;
  }, [currentChatId]);

  return {
    navigateToNewChat,
    getPendingMessage,
    isNewChat: currentChatId === "new",
  };
}
