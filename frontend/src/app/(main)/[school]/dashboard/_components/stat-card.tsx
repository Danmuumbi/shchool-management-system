'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { motion } from 'framer-motion';
import { Users, GraduationCap, DollarSign, LucideIcon } from 'lucide-react';
import React from 'react';

const iconMap: Record<string, LucideIcon> = {
  "Total Students": GraduationCap,
  "Total Teachers": Users,
  "Fees Due": DollarSign,
};

interface StatCardProps {
  title: string;
  value: string;
}

export const StatCard = ({ title, value }: StatCardProps) => {
  const Icon = iconMap[title];

  return (
    <motion.div whileHover={{ y: -5, scale: 1.02 }} transition={{ duration: 0.2 }}>
      <Card className="relative overflow-hidden bg-black border-2 border-green-500/20 hover:border-green-500/40 transition-all duration-300">
        {/* Glow effect */}
        <div className="absolute inset-0 bg-linear-to-br from-green-500/5 via-transparent to-transparent" />
        
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 relative z-10">
          <CardTitle className="text-sm font-medium text-gray-400">
            {title}
          </CardTitle>
          {Icon && <Icon className="h-6 w-6 text-green-500" />}
        </CardHeader>
        <CardContent className="relative z-10">
          <div className="text-3xl font-bold text-white">{value}</div>
        </CardContent>
      </Card>
    </motion.div>
  );
};