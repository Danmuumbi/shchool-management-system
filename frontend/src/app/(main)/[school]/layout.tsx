import React from 'react';
import { PageWrapper } from '../_components/page-wrapper';
import { Sidebar } from '../_components/sidebar';
import { DashboardNavbar } from '../_components/dashboard-navbar';

import schools from '@/lib/dummy/schools.json';
import dashboardData from '@/lib/dummy/dashboard.json';

type DashboardData = {
  modules: { title: string; href: string; icon: string }[];
};

const getSchoolData = (schoolId: string) => {
  return schools.find((s) => s.id === schoolId);
};

const getDashboardData = (schoolId: string): DashboardData | undefined => {
  return (dashboardData as Record<string, DashboardData>)[schoolId];
};

export default async function SchoolLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ school: string }>;
}) {
  const { school: schoolId } = await params;
  const school = getSchoolData(schoolId);
  const dashboard = getDashboardData(schoolId);

  if (!school || !dashboard) {
    return (
      <div className="flex h-screen items-center justify-center bg-white text-red-500">
        School data could not be loaded.
      </div>
    );
  }

  return (
    <div className="min-h-screen w-full bg-white">
      <div className="hidden md:flex h-full w-72 flex-col fixed inset-y-0 z-50">
        <Sidebar
          schoolId={schoolId}
          schoolName={school.name}
          modules={dashboard.modules}
        />
      </div>

      <main className="md:pl-72 h-full bg-white">
        <DashboardNavbar
          schoolId={schoolId}
          schoolName={school.name}
          modules={dashboard.modules}
        />
        <div className="relative z-10 p-4 sm:p-6 md:p-8 bg-white">
          <PageWrapper>{children}</PageWrapper>
        </div>
      </main>
    </div>
  );
}