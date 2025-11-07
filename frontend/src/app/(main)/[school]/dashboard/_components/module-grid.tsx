import React from 'react';
import {
  Users,
  GraduationCap,
  DollarSign,
  Calendar,
  BrainCircuit,
  MessageSquare,
  Clock,
  Library,
  Settings,
  Component, // Fallback icon
  LucideIcon,
} from 'lucide-react';
import Link from 'next/link';
import { Card, CardHeader, CardTitle } from '@/components/ui/card';

// --- Icon Mapping ---
// This allows us to dynamically render icons based on the JSON string
const iconMap: Record<string, LucideIcon> = {
  Users,
  GraduationCap,
  DollarSign,
  Calendar,
  BrainCircuit,
  MessageSquare,
  Clock,
  Library,
  Settings,
};


interface Module {
  title: string;
  href: string;
  icon: string;
}

interface ModuleGridProps {
  modules: Module[];
  schoolId: string;
}

export const ModuleGrid = ({ modules, schoolId }: ModuleGridProps) => {
  return (
    <div>
      <h2 className="text-2xl font-semibold tracking-tight mb-4 text-gray-900 dark:text-white">
        Manage Your School
      </h2>
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
        {modules.map((module) => {
          const Icon = iconMap[module.icon] || Component; // Use fallback icon if not found
          return (
            <Link key={module.title} href={`/${schoolId}${module.href}`}>
              <Card className="hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors duration-200">
                <CardHeader className="flex flex-col items-center justify-center text-center p-4">
                  <Icon className="h-8 w-8 mb-2 text-green-600" />
                  <CardTitle className="text-sm font-medium text-gray-700 dark:text-gray-300">
                    {module.title}
                  </CardTitle>
                </CardHeader>
              </Card>
            </Link>
          );
        })}
      </div>
    </div>
  );
};