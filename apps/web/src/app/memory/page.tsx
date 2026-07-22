import Navbar from '@/components/layout/Navbar';
import Sidebar from '@/components/layout/Sidebar';

export default function MemoryIndex() {
  return (
    <div className="min-h-screen bg-gray-50/50 dark:bg-[#0a0a0a] text-gray-900 dark:text-gray-100">
      <Navbar />
      <div className="container mx-auto flex">
        <Sidebar />
        <main className="flex-1 p-6">
          <div className="mb-8">
            <h1 className="text-3xl font-bold mb-2">Memory Index</h1>
            <p className="text-gray-600 dark:text-gray-400">Global Pricing for DRAM, NAND, and HBM</p>
          </div>
          
          <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-8 text-center text-gray-500">
            <p>Memory pricing data is being aggregated. (API integration pending)</p>
          </div>
        </main>
      </div>
    </div>
  );
}
