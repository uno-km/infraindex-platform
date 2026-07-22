"use client";
import { useEffect, useState } from 'react';
import Navbar from '@/components/layout/Navbar';
import Sidebar from '@/components/layout/Sidebar';

export default function ReportsIndex() {
  const [brief, setBrief] = useState<any>(null);

  useEffect(() => {
    // In production, fetch from process.env.NEXT_PUBLIC_API_URL
    fetch('http://localhost:8000/api/v1/reports/daily-brief')
      .then(res => res.json())
      .then(data => setBrief(data))
      .catch(err => console.error("Error fetching brief:", err));
  }, []);

  return (
    <div className="min-h-screen bg-gray-50/50 dark:bg-[#0a0a0a] text-gray-900 dark:text-gray-100">
      <Navbar />
      <div className="container mx-auto flex">
        <Sidebar />
        <main className="flex-1 p-6">
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold mb-2">Macro Intelligence</h1>
              <p className="text-gray-600 dark:text-gray-400">Daily Global Datacenter & Hardware Reports</p>
            </div>
            <div className="flex space-x-4">
              <a href="http://localhost:8000/api/v1/reports/excel" className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-md font-medium flex items-center transition-colors">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                Export Excel
              </a>
              <a href="http://localhost:8000/api/v1/reports/word" className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md font-medium flex items-center transition-colors">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                Daily Word Brief
              </a>
            </div>
          </div>
          
          {brief ? (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* News Section */}
              <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
                <h2 className="text-xl font-bold mb-4 flex items-center text-blue-600 dark:text-blue-400">
                  <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path></svg>
                  Global Datacenter News
                </h2>
                <div className="space-y-4">
                  {brief.news.map((item: any, idx: number) => (
                    <div key={idx} className="border-b border-gray-100 dark:border-gray-700 pb-3 last:border-0">
                      <p className="font-medium text-gray-900 dark:text-gray-100">{item.title}</p>
                      <div className="flex justify-between text-sm text-gray-500 mt-1">
                        <span>{item.source}</span>
                        <span>{item.date}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Power Section */}
              <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
                <h2 className="text-xl font-bold mb-4 flex items-center text-yellow-600 dark:text-yellow-500">
                  <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                  Industrial Power Costs
                </h2>
                <div className="space-y-4">
                  {brief.power.map((item: any, idx: number) => (
                    <div key={idx} className="flex justify-between items-center border-b border-gray-100 dark:border-gray-700 pb-3 last:border-0">
                      <span className="font-medium">{item.region}</span>
                      <div className="text-right">
                        <div className="font-bold">${item.cost_per_kwh_usd.toFixed(3)} / kWh</div>
                        <span className={`text-xs px-2 py-1 rounded-full ${item.trend === 'rising' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
                          {item.trend.toUpperCase()}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Memory Section */}
              <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 lg:col-span-2">
                <h2 className="text-xl font-bold mb-4 flex items-center text-purple-600 dark:text-purple-400">
                  <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"></path></svg>
                  HBM & Memory Spot Prices
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {brief.memory.map((item: any, idx: number) => (
                    <div key={idx} className="p-4 border border-gray-100 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-900/50">
                      <div className="text-sm text-gray-500 mb-1">{item.component}</div>
                      <div className="text-2xl font-bold">${item.price_usd.toLocaleString()}</div>
                      <div className="text-xs mt-2 text-red-500">{item.status.replace('_', ' ').toUpperCase()}</div>
                    </div>
                  ))}
                </div>
              </div>

            </div>
          ) : (
            <div className="flex justify-center py-20">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
