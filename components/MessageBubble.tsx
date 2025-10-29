
import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import type { Message } from '../types.ts';
import { UserIcon, BotIcon } from './icons.tsx';

interface MessageBubbleProps {
  message: Message;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.role === 'user';

  if (isUser) {
    return (
      <div className="flex justify-end items-start gap-2.5">
        <div className="flex flex-col gap-1 w-full max-w-[480px]">
          <div className="leading-1.5 p-4 bg-blue-600 rounded-s-xl rounded-ee-xl">
            <p className="text-sm font-normal text-white">{message.text}</p>
          </div>
        </div>
        <div className="flex items-center justify-center h-10 w-10 rounded-full bg-slate-200 text-slate-600 flex-shrink-0">
          <UserIcon className="h-6 w-6" />
        </div>
      </div>
    );
  }

  // Bot message
  return (
    <div className="flex justify-start items-start gap-2.5">
      <div className="flex items-center justify-center h-10 w-10 rounded-full bg-blue-600 text-white flex-shrink-0">
        <BotIcon className="h-6 w-6" />
      </div>
      <div className="flex flex-col gap-1 w-full max-w-[480px]">
        <div className="leading-1.5 p-4 border-slate-200 bg-slate-100 rounded-e-xl rounded-es-xl">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            className="prose prose-sm max-w-none prose-slate prose-p:before:content-none prose-p:after:content-none"
            components={{
              a: ({node, ...props}) => <a {...props} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline" />,
              ul: ({node, ...props}) => <ul {...props} className="list-disc list-inside" />,
              ol: ({node, ...props}) => <ol {...props} className="list-decimal list-inside" />,
            }}
          >
            {message.text}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  );
};
