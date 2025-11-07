import React from 'react';

// This layout will eventually hold the sidebar and header for the dashboard.
// For now, it provides the basic structure and background color.

export default function SchoolLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen w-full bg-gray-50 dark:bg-gray-950">
      {/* In the future, a Sidebar and Header component would go here */}
      <main className="p-4 sm:p-6 md:p-8">
        {children}
      </main>
    </div>
  );
}