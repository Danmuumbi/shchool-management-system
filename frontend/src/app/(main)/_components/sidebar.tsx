'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import {
  LayoutDashboard, Users, GraduationCap, DollarSign, Calendar, BrainCircuit,
  MessageSquare, Clock, Library, Settings, Component, LucideIcon, School,
} from 'lucide-react';
import { cn } from '@/lib/utils';

const iconMap: Record<string, LucideIcon> = {
  "/dashboard": LayoutDashboard,
  "/teachers": Users,
  "/students": GraduationCap,
  "/fees": DollarSign,
  "/events": Calendar,
  "/reports": BrainCircuit,
  "/messages": MessageSquare,
  "/timetable": Clock,
  "/library": Library,
  "/settings": Settings,
};

interface Module {
  title: string;
  href: string;
}

interface SidebarProps {
  schoolId: string;
  schoolName: string;
  modules: Module[];
  className?: string;
}

export const Sidebar = ({ schoolId, schoolName, modules, className }: SidebarProps) => {
  const pathname = usePathname();

  const navItems = [{ title: 'Dashboard', href: '/dashboard' }, ...modules];

  return (
    <div className={cn("h-full bg-black border-r-2 border-green-500/20 flex flex-col", className)}>
      <div className="p-6 flex flex-col items-center border-b-2 border-green-500/20">
        <div className="p-3 bg-green-900/50 border border-green-500/30 rounded-lg mb-3">
            <School className="h-10 w-10 text-green-400" />
        </div>
        <h1 className="text-xl font-bold text-white">{schoolName}</h1>
        <p className="text-xs text-green-400">Management Portal</p>
      </div>
      
      <nav className="flex-1 px-4 py-6 space-y-2">
        {navItems.map((item, index) => {
          const Icon = iconMap[item.href] || Component;
          const fullPath = `/${schoolId}${item.href}`;
          const isActive = pathname === fullPath;

          return (
            <motion.div
              key={item.href}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 }}
            >
              <Link
                href={fullPath}
                className={cn(
                  "flex items-center gap-3 rounded-md px-4 py-3 text-sm font-medium transition-all duration-200 ease-in-out",
                  isActive
                    ? "bg-green-500/20 text-green-300 scale-105 shadow-lg shadow-green-900/50"
                    : "text-gray-400 hover:bg-white/10 hover:text-white"
                )}
              >
                <Icon className="h-5 w-5" />
                <span>{item.title}</span>
              </Link>
            </motion.div>
          );
        })}
      </nav>

      <div className="p-4 border-t-2 border-green-500/20 mt-auto">
        <p className="text-xs text-center text-gray-500">&copy; 2025 EvolTechs</p>
      </div>
    </div>
  );
};