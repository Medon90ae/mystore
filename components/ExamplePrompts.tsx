
import React from 'react';
import { EXAMPLE_PROMPTS } from '../constants.ts';
import { SparklesIcon } from './icons.tsx';

interface ExamplePromptsProps {
  onPromptClick: (prompt: string) => void;
  disabled: boolean;
}

export const ExamplePrompts: React.FC<ExamplePromptsProps> = ({ onPromptClick, disabled }) => {
  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200">
      <h2 className="text-xl font-semibold text-slate-700 mb-1">Welcome to FinBot!</h2>
      <p className="text-slate-500 mb-6">I can help you understand investment accounts. Get started by asking a question below or type your own.</p>
      <div className="space-y-3">
        {EXAMPLE_PROMPTS.map((prompt, index) => (
          <button
            key={index}
            onClick={() => onPromptClick(prompt)}
            disabled={disabled}
            className="w-full text-left p-4 bg-slate-50 hover:bg-blue-100 rounded-lg transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed group"
          >
            <p className="font-medium text-slate-700 group-hover:text-blue-700">{prompt}</p>
          </button>
        ))}
      </div>
      <div className="mt-6 text-center text-sm text-slate-400 flex items-center justify-center gap-2">
        <SparklesIcon className="h-4 w-4" />
        <span>Powered by Gemini</span>
      </div>
    </div>
  );
};
