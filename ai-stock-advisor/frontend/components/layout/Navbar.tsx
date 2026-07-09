"use client";

import ThemeToggle from "@/components/theme/ThemeToggle";

export default function Navbar() {
  return (
    <header className="h-16 border-b px-6 flex items-center justify-between bg-white dark:bg-slate-950">
      <h1 className="text-2xl font-bold">
        AI Stock Advisor
      </h1>

      <ThemeToggle />
    </header>
  );
}