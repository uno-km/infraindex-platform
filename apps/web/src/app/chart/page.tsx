import Navbar from '@/components/layout/Navbar';
import Sidebar from '@/components/layout/Sidebar';
import PriceChart from '@/components/chart/PriceChart';

export default function ChartIndex() {
  return (
    <div className="min-h-screen bg-gray-50/50 dark:bg-[#0a0a0a] text-gray-900 dark:text-gray-100">
      <Navbar />
      <div className="container mx-auto flex">
        <Sidebar selectedCategory="all" setSelectedCategory={() => {}} />
        <main className="flex-1 p-6">
          <div className="mb-8">
            <h1 className="text-3xl font-bold mb-2">Price Charts</h1>
            <p className="text-gray-600 dark:text-gray-400">High-performance time-series analysis for GPU rentals.</p>
          </div>
          
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
            <PriceChart gpuModelId="H100" />
            <PriceChart gpuModelId="A100" />
          </div>
        </main>
      </div>
    </div>
  );
}
