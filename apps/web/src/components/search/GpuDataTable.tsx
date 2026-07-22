"use client";

import { useEffect, useState } from 'react';

export default function GpuDataTable() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/search/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ sort_by: "price_asc" })
        });
        const json = await response.json();
        if (json.results) {
          setData(json.results);
        }
      } catch (e) {
        console.error("Failed to fetch GPU data", e);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) return <div className="p-8 text-center text-gray-500">Loading GPU prices from database...</div>;

  return (
    <div className="overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-800 shadow-sm">
      <table className="w-full text-left text-sm whitespace-nowrap">
        <thead className="bg-gray-50 dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800">
          <tr>
            <th className="p-4 font-semibold text-gray-700 dark:text-gray-300">Provider</th>
            <th className="p-4 font-semibold text-gray-700 dark:text-gray-300">Configuration</th>
            <th className="p-4 font-semibold text-gray-700 dark:text-gray-300">Total VRAM</th>
            <th className="p-4 font-semibold text-gray-700 dark:text-gray-300">Plan Type</th>
            <th className="p-4 font-semibold text-gray-700 dark:text-gray-300 text-right">Hourly Price</th>
            <th className="p-4 font-semibold text-gray-700 dark:text-gray-300 text-right">Est. Monthly</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200 dark:divide-gray-800 bg-white dark:bg-black/20">
          {data.length === 0 ? (
            <tr><td colSpan={6} className="p-4 text-center text-gray-500">No data available.</td></tr>
          ) : (
            data.map((row: any) => {
              // Extract data from nested Pydantic response
              const provider = row.offering?.provider?.name || "Unknown";
              const model = row.offering?.machine_type_name || "Unknown";
              const type = row.plan_type || "On-Demand";
              
              // Get latest observation for pricing
              const latestObs = row.observations && row.observations.length > 0 
                ? row.observations[row.observations.length - 1] 
                : null;
                
              const hourlyPrice = latestObs ? `$${latestObs.normalized_hourly_price.toFixed(2)}/hr` : "N/A";
              const monthlyPrice = latestObs ? `$${latestObs.normalized_monthly_price.toFixed(2)}/mo` : "N/A";
              
              // Calculate VRAM
              let totalVram = 0;
              if (row.offering?.gpu_configuration) {
                for (const config of row.offering.gpu_configuration) {
                  totalVram += (config.count * (config.variant?.vram_gb || 0));
                }
              }

              return (
                <tr key={row.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                  <td className="p-4 font-medium">{provider}</td>
                  <td className="p-4 text-blue-600 dark:text-blue-400 font-medium cursor-pointer hover:underline">{model}</td>
                  <td className="p-4">{totalVram > 0 ? `${totalVram}GB` : "N/A"}</td>
                  <td className="p-4">
                    <span className="inline-flex items-center rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-800 dark:bg-blue-900/30 dark:text-blue-300">
                      {type === "secure_cloud" ? "Secure Cloud" : type === "community_cloud" ? "Community" : "On-Demand"}
                    </span>
                  </td>
                  <td className="p-4 text-right font-mono font-medium">{hourlyPrice}</td>
                  <td className="p-4 text-right font-mono text-gray-500 dark:text-gray-400">{monthlyPrice}</td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>
    </div>
  );
}
