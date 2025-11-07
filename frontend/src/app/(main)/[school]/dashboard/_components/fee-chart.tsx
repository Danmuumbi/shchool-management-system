'use client';

import React from 'react';
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from 'recharts';
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription
} from '@/components/ui/card';


interface FeeChartProps {
  data: { month: string; collected: number }[];
}

export const FeeChart = ({ data }: FeeChartProps) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Fee Collection Analysis</CardTitle>
        <CardDescription>Total amount collected per month.</CardDescription>
      </CardHeader>
      <CardContent className="pl-2">
        <ResponsiveContainer width="100%" height={350}>
          <BarChart data={data}>
            <XAxis
              dataKey="month"
              stroke="#525252"
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis
              stroke="#525252"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={(value) => `KES ${Number(value) / 1000}k`}
            />
            <Tooltip
              cursor={{ fill: 'transparent' }}
              contentStyle={{
                backgroundColor: 'rgba(255, 255, 255, 0.8)',
                border: '1px solid #ccc',
                borderRadius: '0.5rem',
              }}
            />
            <Bar dataKey="collected" fill="#16a34a" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};