
import { useState, useCallback } from 'react';
import type { Message } from '../types.ts';

// --- MOCK FIREBASE AUTH ---
// In a real app, you would use the Firebase SDK to get the current user and their ID token.
// For example: `await auth.currentUser.getIdToken()`
const getMockIdToken = async (): Promise<string | null> => {
  console.warn("Using mock Firebase ID token. Replace with actual Firebase Auth.");
  // In a real scenario, if there's no user, you'd return null and handle the unauthenticated state.
  return "mock-firebase-id-token"; 
};
// --- END MOCK ---

export const useGeminiChat = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  // The chat history is now managed server-side, so we don't need to keep a `chatRef` here.

  const sendMessageStream = useCallback(async function* (params: { message: string, history: Message[] }) {
    setLoading(true);
    setError(null);

    const idToken = await getMockIdToken();
    if (!idToken) {
      const errText = "Authentication failed: User is not signed in.";
      setError(errText);
      setLoading(false);
      throw new Error(errText);
    }

    try {
      // The backend API URL would be configured, e.g., from an environment variable.
      const API_URL = '/api/chat'; // Assuming a proxy is set up for local dev. In production, this would be your Cloud Run URL.

      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${idToken}`,
        },
        body: JSON.stringify({
          prompt: params.message,
          history: params.history, // Send previous messages for context
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || `Request failed with status ${response.status}`);
      }

      // The backend now streams the response
      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error("Failed to get response reader.");
      }
      const decoder = new TextDecoder();
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        // Assuming the backend streams plain text chunks
        yield { text: chunk };
      }

    } catch (e) {
      console.error("Error sending message to backend:", e);
      const errText = e instanceof Error ? e.message : "Failed to get response from the server.";
      setError(errText);
      throw new Error(errText);
    } finally {
      setLoading(false);
    }
  }, []);

  // The App component will now manage the history and pass it to sendMessageStream
  return { sendMessageStream, loading, error };
};
