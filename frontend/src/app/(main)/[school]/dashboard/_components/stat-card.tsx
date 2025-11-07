import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import React from 'react';

interface StatCardProps {
  title: string;
  value: string;
}

export const StatCard = ({ title, value }: StatCardProps) => {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-gray-500 dark:text-gray-400">
          {title}
        </CardTitle>
        {/* An icon could go here */}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold text-gray-900 dark:text-white">{value}</div>
      </CardContent>
    </Card>
  );
};