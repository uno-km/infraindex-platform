"use client";

import React, { useEffect, useState } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface ChartDataPoint {
  timestamp: string;
  min_price: number;
  max_price: number;
  avg_price: number;
}

interface ChartSeriesResponse {
  gpu_model: string;
  provider: string;
  data: ChartDataPoint[];
}

export default function PriceChart({ gpuModelId = 'H100' }: { gpuModelId?: string }) {
  const [series, setSeries] = useState<ChartSeriesResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchChartData() {
      try {
        const res = await fetch(`http://127.0.0.1:8000/api/v1/chart/price-series?gpu_model_id=${gpuModelId}`);
        const data = await res.json();
        setSeries(data);
      } catch (err) {
        console.error("Failed to load chart data", err);
      } finally {
        setLoading(false);
      }
    }
    fetchChartData();
  }, [gpuModelId]);

  if (loading) {
    return <div className="h-64 flex items-center justify-center text-gray-500">Loading High-Performance Chart...</div>;
  }

  if (!series || series.length === 0) {
    return <div className="h-64 flex items-center justify-center text-gray-500">No chart data available.</div>;
  }

  // Format data for Recharts (Flatten the structure for Recharts XAxis)
  const chartData = series[0].data.map((pt) => ({
    time: new Date(pt.timestamp).toLocaleDateString(),
    "Min Price": pt.min_price,
    "Avg Price": pt.avg_price,
    "Max Price": pt.max_price
  }));

  const currentAvg = chartData[chartData.length - 1]?.["Avg Price"] || 0;
  const previousAvg = chartData[chartData.length - 2]?.["Avg Price"] || currentAvg;
  const change = currentAvg - previousAvg;
  const percentChange = previousAvg > 0 ? (change / previousAvg) * 100 : 0;

  return (
    <div className="bg-white dark:bg-[#111111] border border-gray-200 dark:border-gray-800 rounded-xl p-6 shadow-sm">
      <div className="flex justify-between items-start mb-6">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100">{series[0].gpu_model} Price Trend</h2>
          <p className="text-sm text-gray-500 mt-1">Aggregated across {series[0].provider}</p>
        </div>
        <div className="text-right">
          <div className="text-2xl font-mono font-bold text-gray-900 dark:text-gray-100">
            ${currentAvg.toFixed(2)}/hr
          </div>
          <div className={`flex items-center justify-end text-sm font-medium mt-1 ${change > 0 ? 'text-red-500' : change < 0 ? 'text-green-500' : 'text-gray-500'}`}>
            {change > 0 ? <TrendingUp className="w-4 h-4 mr-1" /> : change < 0 ? <TrendingDown className="w-4 h-4 mr-1" /> : <Minus className="w-4 h-4 mr-1" />}
            {Math.abs(percentChange).toFixed(2)}%
          </div>
        </div>
      </div>
      
      <div className="h-72 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 5, right: 0, left: -20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#333" opacity={0.3} />
            <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#888' }} dy={10} />
            <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#888' }} tickFormatter={(val) => `$${val}`} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#1f2937', borderColor: '#374151', color: '#f3f4f6', borderRadius: '8px' }}
              itemStyle={{ color: '#e5e7eb' }}
            />
            <Legend verticalAlign="top" height={36} iconType="circle" />
            <Line type="monotone" dataKey="Avg Price" stroke="#3b82f6" strokeWidth={3} dot={{ r: 4, fill: '#3b82f6', strokeWidth: 2, stroke: '#fff' }} activeDot={{ r: 6 }} />
            <Line type="monotone" dataKey="Min Price" stroke="#10b981" strokeWidth={2} strokeDasharray="5 5" dot={false} />
            <Line type="monotone" dataKey="Max Price" stroke="#ef4444" strokeWidth={2} strokeDasharray="5 5" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
