"use client";

import {
  LayoutDashboard,
  Search,
  Newspaper,
  Briefcase,
  Settings
} from "lucide-react";

const menus = [
  {
    name: "Dashboard",
    icon: LayoutDashboard,
  },
  {
    name: "Search",
    icon: Search,
  },
  {
    name: "News",
    icon: Newspaper,
  },
  {
    name: "Portfolio",
    icon: Briefcase,
  },
  {
    name: "Settings",
    icon: Settings,
  },
];

export default function Sidebar() {
  return (
    <aside className="w-64 border-r bg-white dark:bg-slate-950 h-[calc(100vh-64px)]">
      <nav className="p-4 space-y-2">
        {menus.map((menu) => {
          const Icon = menu.icon;

          return (
            <button
              key={menu.name}
              className="w-full flex items-center gap-3 rounded-lg px-3 py-2 hover:bg-gray-100 dark:hover:bg-slate-800 transition"
            >
              <Icon size={18} />

              {menu.name}
            </button>
          );
        })}
      </nav>
    </aside>
  );
}