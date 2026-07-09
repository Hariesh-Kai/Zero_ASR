import MainLayout from "@/components/layout/MainLayout";

export default function Home() {
  return (
    <MainLayout>
      <h1 className="text-3xl font-bold">
        Welcome to AI Stock Advisor
      </h1>

      <p className="mt-4 text-gray-600 dark:text-gray-400">
        Intelligent stock market analysis powered by AI.
      </p>
    </MainLayout>
  );
}