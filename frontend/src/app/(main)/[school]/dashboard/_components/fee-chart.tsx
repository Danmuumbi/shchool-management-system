'use client';

import React from 'react';
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from '@/components/ui/card';

interface FeeChartProps {
  data: { month: string; collected: number }[];
}

export const FeeChart = ({ data }: FeeChartProps) => {
  return (
    <Card className="bg-black border-2 border-green-500/20 hover:border-green-500/30 transition-colors duration-300">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-white">
          Fee Collection Overview
        </CardTitle>
        <CardDescription className="text-gray-400">
          Monthly fee collection for the last 6 months.
        </CardDescription>
      </CardHeader>
      <CardContent className="pl-2">
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(34, 197, 94, 0.1)" />
            <XAxis
              dataKey="month"
              stroke="#9ca3af"
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis
              stroke="#9ca3af"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={(value) => `KES ${Number(value) / 1000}k`}
            />
            <Tooltip
              cursor={{ fill: 'rgba(34, 197, 94, 0.1)' }}
              contentStyle={{
                backgroundColor: '#000000',
                border: '2px solid rgba(34, 197, 94, 0.3)',
                borderRadius: '0.5rem',
                color: '#ffffff',
              }}
              labelStyle={{ color: '#22c55e' }}
            />
            <Bar
              dataKey="collected"
              fill="url(#greenGradient)"
              radius={[8, 8, 0, 0]}
            />
            <defs>
              <linearGradient id="greenGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#22c55e" stopOpacity={1}/>
                <stop offset="100%" stopColor="#16a34a" stopOpacity={0.8}/>
              </linearGradient>
            </defs>
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};