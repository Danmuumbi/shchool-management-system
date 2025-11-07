import React from 'react';
import { WelcomeHeader } from '@/app/(main)/[school]/dashboard/_components/welcome-header';
import { StatCard } from '@/app/(main)/[school]/dashboard/_components/stat-card';
import { FeeChart } from '@/app/(main)/[school]/dashboard/_components/fee-chart';
import { ModuleGrid } from '@/app/(main)/[school]/dashboard/_components/module-grid';   

// --- Mock Data Imports ---
// In a real app, this would come from an API call
import schools from '@/lib/dummy/schools.json';
import dashboardData from '@/lib/dummy/dashboard.json';

// --- Type Definitions for our dummy data ---
type School = {
  id: string;
  name: string;
};

type DashboardData = {
  stats: { students: number; teachers: number; fees_due: string };
  chartData: { month: string; collected: number }[];
  modules: { title: string; href: string; icon: string }[];
};

// --- Mock Data Fetching Functions ---
const getSchoolData = (schoolId: string): School | undefined => {
  return schools.find((s) => s.id === schoolId);
};

const getDashboardData = (schoolId: string): DashboardData | undefined => {
  // TypeScript type assertion to handle dynamic keys
  return (dashboardData as Record<string, DashboardData>)[schoolId];
};


export default function DashboardPage({
  params,
}: {
  params: { school: string };
}) {
  const schoolId = params.school;
  const school = getSchoolData(schoolId);
  const dashboard = getDashboardData(schoolId);

  // Simple error handling if data isn't found
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

      {/* Stats Cards Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <StatCard title="Total Students" value={dashboard.stats.students.toString()} />
        <StatCard title="Total Teachers" value={dashboard.stats.teachers.toString()} />
        <StatCard title="Fees Due" value={dashboard.stats.fees_due} />
      </div>
      
      {/* Main Grid for Chart and other future items */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          <div className="lg:col-span-2">
             <FeeChart data={dashboard.chartData} />
          </div>
          {/* You can add more components here later */}
      </div>

      <ModuleGrid modules={dashboard.modules} schoolId={schoolId} />
    </div>
  );
}