
import React, { useState, useCallback } from 'react';
import { ChatWindow } from './components/ChatWindow.tsx';
import { ExamplePrompts } from './components/ExamplePrompts.tsx';
import { Header } from './components/Header.tsx';
import { useGeminiChat } from './hooks/useGeminiChat.ts';
import type { Message } from './types.ts';

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const { sendMessageStream, loading, error } = useGeminiChat();

  const handleSendMessage = useCallback(async (text: string) => {
    if (loading || !text.trim()) return;

    const userMessage: Message = { role: 'user', text };
    // Pass the current message history to the hook
    const currentHistory = [...messages]; 
    
    setMessages(prev => [...prev, userMessage]);

    // Add a placeholder for the bot's response
    const botMessage: Message = { role: 'model', text: '' };
    setMessages(prev => [...prev, botMessage]);

    try {
      const stream = sendMessageStream({ message: text, history: currentHistory });
      let fullResponse = '';

      for await (const chunk of stream) {
        fullResponse += chunk.text;
        setMessages(prev => {
          const newMessages = [...prev];
          const lastMessage = newMessages[newMessages.length - 1];
          if (lastMessage && lastMessage.role === 'model') {
            newMessages[newMessages.length - 1] = { ...lastMessage, text: fullResponse };
          }
          return newMessages;
        });
      }
    } catch (e) {
      console.error("Error streaming response:", e);
      setMessages(prev => {
        const newMessages = [...prev];
        const lastMessage = newMessages[newMessages.length - 1];
        if (lastMessage && lastMessage.role === 'model') {
            newMessages[newMessages.length - 1] = { ...lastMessage, text: "Sorry, I encountered an error. Please try again." };
        }
        return newMessages;
      });
    }
  }, [loading, sendMessageStream, messages]);

  return (
    <div className="min-h-screen bg-slate-100 font-sans text-slate-800 flex flex-col">
      <Header />
      <main className="flex-grow container mx-auto p-4 lg:p-8 flex flex-col lg:flex-row gap-8">
        <div className="lg:w-1/3 lg:pr-8">
          <ExamplePrompts onPromptClick={handleSendMessage} disabled={loading} />
        </div>
        <div className="lg:w-2/3 flex flex-col h-[80vh] lg:h-auto">
          <ChatWindow
            messages={messages}
            onSendMessage={handleSendMessage}
            isLoading={loading}
            error={error}
          />
        </div>
      </main>
    </div>
  );
}
