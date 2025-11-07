'use client';

import { Menu } from 'lucide-react';
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet';
import { Button } from '@/components/ui/button';
import { Sidebar } from './sidebar';

interface DashboardNavbarProps {
  schoolId: string;
  schoolName: string;
  modules: { title: string; href: string }[];
}

export const DashboardNavbar = ({ schoolId, schoolName, modules }: DashboardNavbarProps) => {
  return (
    <header className="md:hidden sticky top-0 h-16 flex items-center gap-4 border-b-2 border-green-500/20 bg-black/80 backdrop-blur-sm px-4 z-50">
      <Sheet>
        <SheetTrigger asChild>
          <Button variant="ghost" size="icon" className="text-white hover:bg-white/10">
            <Menu className="h-6 w-6" />
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="p-0 w-72 bg-black border-r-2 border-green-500/20">
          <Sidebar
            schoolId={schoolId}
            schoolName={schoolName}
            modules={modules}
          />
        </SheetContent>
      </Sheet>
      <h1 className="text-lg font-bold text-white">{schoolName}</h1>
    </header>
  );
};