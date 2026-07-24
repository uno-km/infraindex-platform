"use client";

import React from 'react';
import { Table as TableIcon } from 'lucide-react';

export default function DataViewerTab() {
  // In a real app, you would fetch data from /api/v1/gpus or similar
  return (
    <div className="space-y-6 text-white">
      <h2 className="text-xl font-semibold flex items-center gap-2 mb-4">
        <TableIcon className="w-5 h-5 text-indigo-400" />
        Data Viewer
      </h2>
      <p className="text-gray-400 text-sm mb-4">
        This is a placeholder for the data viewer table. In the future, this tab will display raw crawled data, anomalies, and metrics.
      </p>

      <div className="bg-[#1a1a1a] border border-gray-800 rounded-xl overflow-hidden">
        <table className="w-full text-left text-sm text-gray-300">
          <thead className="bg-[#222] text-gray-400 uppercase">
            <tr>
              <th className="px-4 py-3">Provider</th>
              <th className="px-4 py-3">GPU Model</th>
              <th className="px-4 py-3">Price (Hourly)</th>
              <th className="px-4 py-3">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr className="border-b border-gray-800 hover:bg-[#252525]">
              <td className="px-4 py-3 font-bold text-blue-400">AWS</td>
              <td className="px-4 py-3">A100 80GB</td>
              <td className="px-4 py-3 font-mono">$4.09</td>
              <td className="px-4 py-3"><span className="text-green-400">Available</span></td>
            </tr>
            <tr className="border-b border-gray-800 hover:bg-[#252525]">
              <td className="px-4 py-3 font-bold text-green-500">Lambda</td>
              <td className="px-4 py-3">H100 PCIe</td>
              <td className="px-4 py-3 font-mono">$2.49</td>
              <td className="px-4 py-3"><span className="text-red-400">Unavailable</span></td>
            </tr>
            <tr className="border-b border-gray-800 hover:bg-[#252525]">
              <td className="px-4 py-3 font-bold text-orange-500">RunPod</td>
              <td className="px-4 py-3">RTX 4090</td>
              <td className="px-4 py-3 font-mono">$0.44</td>
              <td className="px-4 py-3"><span className="text-green-400">Available</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
