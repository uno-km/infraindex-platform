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
import { TrendingUp, TrendingDown, Minus, Cloud } from 'lucide-react';
import BaseChartLayout from './BaseChartLayout';

interface ChartDataPoint {
  timestamp: string;
  min_price: number;
  max_price: number;
  avg_price: number;
}

interface ChartSeriesResponse {
  model_name: string;
  provider: string;
  data: ChartDataPoint[];
}

export default function LineChartWidget({ 
  hwTyp = 'gpu', 
  modelId = 'H100' 
}: { 
  hwTyp?: 'gpu' | 'cpu' | 'storage' | 'baremetal';
  modelId?: string;
}) {
  const [series, setSeries] = useState<ChartSeriesResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchChartData() {
      try {
        setLoading(true);
        const res = await fetch(`http://127.0.0.1:8000/api/v1/chart/unified-price-series?hw_typ=${hwTyp}&model_id=${modelId}`);
        const data = await res.json();
        setSeries(data);
      } catch (err) {
        console.error("Failed to load chart data", err);
      } finally {
        setLoading(false);
      }
    }
    fetchChartData();
  }, [hwTyp, modelId]);

  const isEmpty = !series || series.length === 0;

  // Header Right Element
  let rightElement = null;
  if (!isEmpty && !loading) {
    const chartData = series[0].data;
    const currentAvg = chartData[chartData.length - 1]?.avg_price || 0;
    const previousAvg = chartData[chartData.length - 2]?.avg_price || currentAvg;
    const change = currentAvg - previousAvg;
    const percentChange = previousAvg > 0 ? (change / previousAvg) * 100 : 0;
    const unit = hwTyp === 'storage' ? '/GB/mo' : '/hr';
    
    rightElement = (
      <div className="text-right">
        <div className="text-2xl font-mono font-black text-slate-900">
          ${currentAvg.toFixed(hwTyp === 'storage' ? 4 : 2)}{unit}
        </div>
        <div className={`flex items-center justify-end text-sm font-bold mt-1 ${change > 0 ? 'text-red-500' : change < 0 ? 'text-emerald-500' : 'text-slate-500'}`}>
          {change > 0 ? <TrendingUp className="w-4 h-4 mr-1" /> : change < 0 ? <TrendingDown className="w-4 h-4 mr-1" /> : <Minus className="w-4 h-4 mr-1" />}
          {Math.abs(percentChange).toFixed(2)}%
        </div>
      </div>
    );
  }

  const title = !isEmpty && !loading ? `${series[0].model_name} ${hwTyp.toUpperCase()} 추이` : `${modelId} 추이`;
  const desc = !isEmpty && !loading ? `Aggregated across ${series[0].provider}` : undefined;

  return (
    <BaseChartLayout
      title={title}
      icon={<Cloud className="text-blue-500" size={20} />}
      description={desc}
      loading={loading}
      empty={isEmpty}
      emptyMessage={`${modelId} (${hwTyp}) 데이터가 없습니다.`}
      rightHeaderElement={rightElement}
    >
      {/* 내부 차트 (Recharts) */}
      {!isEmpty && (
        <ResponsiveContainer width="100%" height="100%">
          <LineChart 
            data={series[0].data.map(pt => ({
              time: new Date(pt.timestamp).toLocaleDateString(),
              "Min Price": pt.min_price,
              "Avg Price": pt.avg_price,
              "Max Price": pt.max_price
            }))} 
            margin={{ top: 15, right: 10, left: -20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
            <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b', fontWeight: 'bold' }} dy={10} />
            <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#64748b', fontWeight: 'bold' }} tickFormatter={(val) => `$${val}`} />
            <Tooltip 
              contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', color: '#0f172a', borderRadius: '12px', fontWeight: 'bold', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
              itemStyle={{ color: '#334155' }}
              formatter={(value: any) => [`$${Number(value).toFixed(hwTyp === 'storage' ? 4 : 2)}`, undefined]}
            />
            <Legend verticalAlign="top" height={36} iconType="circle" wrapperStyle={{ fontWeight: 'bold', fontSize: '13px' }} />
            <Line type="monotone" dataKey="Avg Price" stroke="#4f46e5" strokeWidth={3} dot={{ r: 4, fill: '#4f46e5', strokeWidth: 2, stroke: '#fff' }} activeDot={{ r: 6 }} />
            <Line type="monotone" dataKey="Min Price" stroke="#10b981" strokeWidth={2} strokeDasharray="5 5" dot={false} />
            <Line type="monotone" dataKey="Max Price" stroke="#ef4444" strokeWidth={2} strokeDasharray="5 5" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      )}
    </BaseChartLayout>
  );
}
