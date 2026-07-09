import Navbar from "./Navbar";
import Sidebar from "./Sidebar";

interface Props {
  children: React.ReactNode;
}

export default function MainLayout({
  children,
}: Props) {
  return (
    <div className="min-h-screen bg-white text-black dark:bg-slate-950 dark:text-white transition-colors">
      <Navbar />

      <div className="flex">
        <Sidebar />

        <main className="flex-1 p-8">
          {children}
        </main>
      </div>
    </div>
  );
}