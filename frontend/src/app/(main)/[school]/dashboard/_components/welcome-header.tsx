import { Sparkles } from 'lucide-react';
import React from 'react';

interface WelcomeHeaderProps {
  schoolName: string;
}

export const WelcomeHeader = ({ schoolName }: WelcomeHeaderProps) => {
  return (
    <div className="mb-8">
      <div className="flex items-center gap-3 mb-2">
        <Sparkles className="h-8 w-8 text-green-600" />
        <h1 className="text-5xl font-bold tracking-tight text-gray-900">
          Welcome, <span className="text-green-600">{schoolName}</span>
        </h1>
      </div>
      <p className="text-lg text-gray-600 ml-11">
        Your central hub for school management and insights.
      </p>
    </div>
  );
}

