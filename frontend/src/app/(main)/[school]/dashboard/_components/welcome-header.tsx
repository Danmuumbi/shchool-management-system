import React from 'react';

interface WelcomeHeaderProps {
  schoolName: string;
}

export const WelcomeHeader = ({ schoolName }: WelcomeHeaderProps) => {
  return (
    <div>
      <h1 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-white">
        Welcome, {schoolName}
      </h1>
      <p className="mt-1 text-md text-gray-500 dark:text-gray-400">
        Here is your school&apos;s overview at a glance.
      </p>
    </div>
  );
};