import React from 'react';
import { WelcomeHeader } from './_components/welcome-header';
import { StatCard } from './_components/stat-card';
import { FeeChart } from './_components/fee-chart';
import { ModuleGrid } from './_components/module-grid';

import schools from '@/lib/dummy/schools.json';
import dashboardData from '@/lib/dummy/dashboard.json';

type School = {
  id: string;
  name: string;
};

type DashboardData = {
  stats: { students: number; teachers: number; fees_due: string };
  chartData: { month: string; collected: number }[];
  modules: { title: string; href: string; icon: string }[];
};

const getSchoolData = (schoolId: string): School | undefined => {
  return schools.find((s) => s.id === schoolId);
};

const getDashboardData = (schoolId: string): DashboardData | undefined => {
  return (dashboardData as Record<string, DashboardData>)[schoolId];
};

export default async function DashboardPage({
  params,
}: {
  params: Promise<{ school: string }>;
}) {
  const { school: schoolId } = await params;
  const school = getSchoolData(schoolId);
  const dashboard = getDashboardData(schoolId);

  if (!school || !dashboard) {
    return (
      <div className="flex h-screen items-center justify-center">
        <p className="text-xl text-red-500">
          Error: School data for &quot;{schoolId}&quot; not found.
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-6">
      <WelcomeHeader schoolName={school.name} />

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <StatCard title="Total Students" value={dashboard.stats.students.toString()} />
        <StatCard title="Total Teachers" value={dashboard.stats.teachers.toString()} />
        <StatCard title="Fees Due" value={dashboard.stats.fees_due} />
      </div>
      
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="lg:col-span-2">
             <FeeChart data={dashboard.chartData} />
          </div>
      </div>

      <ModuleGrid modules={dashboard.modules} schoolId={schoolId} />
    </div>
  );
}