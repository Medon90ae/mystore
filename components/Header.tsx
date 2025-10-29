
import React from 'react';
import { BotIcon } from './icons.tsx';

export const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-md">
      <div className="container mx-auto px-4 lg:px-8 py-4 flex items-center gap-3">
        <BotIcon className="h-8 w-8 text-blue-600" />
        <h1 className="text-2xl font-bold text-slate-800">
          FinBot <span className="font-normal text-slate-500">Investment Advisor</span>
        </h1>
      </div>
    </header>
  );
};
