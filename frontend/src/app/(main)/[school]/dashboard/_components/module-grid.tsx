'use client';

import React from 'react';
import Link from 'next/link';
import { motion, type Variants } from 'framer-motion';
import {
  Users, GraduationCap, DollarSign, Calendar, BrainCircuit, MessageSquare,
  Clock, Library, Settings, Component, LucideIcon, ArrowRight,
} from 'lucide-react';

const iconMap: Record<string, LucideIcon> = {
  Users, GraduationCap, DollarSign, Calendar, BrainCircuit, MessageSquare,
  Clock, Library, Settings,
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

const cardVariants: Variants = {
  hidden: { 
    opacity: 0, 
    scale: 0.95 
  },
  visible: {
    opacity: 1,
    scale: 1,
  },
};

export const ModuleGrid = ({ modules, schoolId }: ModuleGridProps) => {
  return (
    <div className="mt-12">
      <h2 className="text-3xl font-bold tracking-tight text-gray-900 mb-6 flex items-center gap-2"></h2>
      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
        {modules.map((module, i) => {
          const Icon = iconMap[module.icon] || Component;
          return (
            <motion.div
              key={module.title}
              variants={cardVariants}
              initial="hidden"
              animate="visible"
              transition={{
                delay: i * 0.05,
                duration: 0.3,
                ease: "easeOut",
              }}
              whileHover={{ scale: 1.05, y: -5 }}
              className="group relative"
            >
              <Link href={`/${schoolId}${module.href}`}>
                {/* Glow effect on hover */}
                <div className="absolute inset-0 bg-green-500/20 rounded-xl blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                
                <div className="relative flex flex-col items-center justify-center p-6 text-center h-full rounded-xl bg-[#000000] border-2 border-green-500/30 group-hover:border-green-500 transition-all duration-300 shadow-lg">
                  <Icon className="h-10 w-10 mb-3 text-green-500 group-hover:text-green-400 transition-colors" />
                  <h3 className="text-sm font-semibold text-white group-hover:text-green-100 transition-colors">
                    {module.title}
                  </h3>
                  <ArrowRight className="absolute bottom-3 right-3 h-4 w-4 text-green-500/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                </div>
              </Link>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};