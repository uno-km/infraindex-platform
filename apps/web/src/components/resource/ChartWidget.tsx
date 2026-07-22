"use client";

import { useMemo, useEffect, useState } from "react";
import dynamic from "next/dynamic";

const Chart = dynamic(() => import("react-apexcharts"), { ssr: false });

interface ChartWidgetProps {
  gpuName: string;
  basePrice: number;
  exchangeRate: number;
  providers: string[];
  period: "DAY" | "WEEK" | "MONTH";
}

export default function ChartWidget({ gpuName, basePrice, exchangeRate, providers, period }: ChartWidgetProps) {
  const [realData, setRealData] = useState<any[]>([]);

  useEffect(() => {
    async function fetchData() {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const res = await fetch(`${apiUrl}/api/v1/chart/candlestick?gpu_model_id=${encodeURIComponent(gpuName)}&days=90`);
        if (res.ok) {
          const data = await res.json();
          setRealData(data);
        }
      } catch (err) {
        console.error("Failed to fetch candlestick data", err);
      }
    }
    fetchData();
  }, [gpuName]);

  const chartData = useMemo(() => {
    if (realData.length === 0) return [];
    const aggregated = [];
    let chunkSize = period === "DAY" ? 1 : period === "WEEK" ? 7 : 30;
    
    for (let i = 0; i < realData.length; i += chunkSize) {
      const chunk = realData.slice(i, i + chunkSize);
      const date = chunk[chunk.length - 1].x;
      const open = chunk[0].y[0];
      const close = chunk[chunk.length - 1].y[3];
      const high = Math.max(...chunk.map(d => d.y[1]));
      const low = Math.min(...chunk.map(d => d.y[2]));
      
      const highPoint = chunk.find(d => d.y[1] === high) || chunk[0];
      const lowPoint = chunk.find(d => d.y[2] === low) || chunk[0];
      const avg = chunk.reduce((acc, curr) => acc + curr.avg, 0) / chunk.length;
      
      aggregated.push({
        x: date,
        y: [
          parseFloat((open * exchangeRate).toFixed(exchangeRate === 1 ? 3 : 0)),
          parseFloat((high * exchangeRate).toFixed(exchangeRate === 1 ? 3 : 0)),
          parseFloat((low * exchangeRate).toFixed(exchangeRate === 1 ? 3 : 0)),
          parseFloat((close * exchangeRate).toFixed(exchangeRate === 1 ? 3 : 0))
        ],
        highProvider: highPoint.highProvider,
        lowProvider: lowPoint.lowProvider,
        avg: parseFloat((avg * exchangeRate).toFixed(exchangeRate === 1 ? 3 : 0))
      });
    }

    const displayCount = period === "DAY" ? 30 : period === "WEEK" ? 12 : 6;
    const finalData = aggregated.slice(-displayCount);

    const smaData = [];
    for (let i = 0; i < finalData.length; i++) {
      if (i < 4) {
        smaData.push({ x: finalData[i].x, y: null });
      } else {
        const sum = finalData.slice(i - 4, i + 1).reduce((acc, curr) => acc + curr.y[3], 0);
        smaData.push({ x: finalData[i].x, y: parseFloat((sum / 5).toFixed(exchangeRate === 1 ? 3 : 0)) });
      }
    }

    return [
      { name: '시세', type: 'candlestick', data: finalData },
      { name: '5일 추세선', type: 'line', data: smaData }
    ];
  }, [exchangeRate, period, realData]);

  const currencySymbol = exchangeRate === 1 ? "$" : "₩";

  const options = {
    chart: { 
      toolbar: { show: false }, 
      fontFamily: 'inherit', 
      background: 'transparent',
      animations: { enabled: false }
    },
    stroke: {
      width: [1, 2],
      curve: 'smooth'
    },
    colors: ['#000000', '#8b5cf6'],
    title: { text: `${gpuName} 가격 변동 추이`, align: 'left', style: { fontSize: '15px', fontWeight: '700', color: '#1e293b' } },
    xaxis: { type: 'datetime', labels: { style: { colors: '#64748b', fontSize: '12px', fontWeight: 500 } }, axisBorder: { show: false }, axisTicks: { show: false } },
    yaxis: { 
      tooltip: { enabled: true }, 
      labels: { style: { colors: '#64748b', fontWeight: 500 }, formatter: (val: number) => `${currencySymbol}${val ? val.toLocaleString() : ''}` } 
    },
    tooltip: {
      shared: true,
      custom: function({seriesIndex, dataPointIndex, w}: any) {
        if (seriesIndex !== 0) return ''; 
        const data = w.globals.initialSeries[0].data[dataPointIndex];
        const lineData = w.globals.initialSeries[1].data[dataPointIndex];
        const [o, h, l, c] = data.y;
        return `
          <div class="p-3 bg-white/90 backdrop-blur-md text-xs text-slate-800 shadow-[0_8px_30px_rgb(0,0,0,0.12)] border border-slate-100 rounded-xl min-w-[170px]">
            <div class="mb-2 font-bold text-slate-500 border-b border-slate-100 pb-1">${new Date(data.x).toLocaleDateString()}</div>
            <div class="mb-1 flex justify-between gap-4"><span>시가 (Open):</span> <strong>${currencySymbol}${o}</strong></div>
            <div class="mb-1 flex justify-between gap-4 text-rose-500">
              <span class="truncate capitalize max-w-[80px]" title="최고가: ${data.highProvider}">고가 (${data.highProvider}):</span> 
              <strong>${currencySymbol}${h}</strong>
            </div>
            <div class="mb-1 flex justify-between gap-4 text-indigo-500">
              <span class="truncate capitalize max-w-[80px]" title="최저가: ${data.lowProvider}">저가 (${data.lowProvider}):</span> 
              <strong>${currencySymbol}${l}</strong>
            </div>
            <div class="mt-1 flex justify-between gap-4 pt-1 border-t border-slate-100"><span>평균 (Avg):</span> <strong>${currencySymbol}${data.avg}</strong></div>
            <div class="mt-1 flex justify-between gap-4"><span>종가 (Close):</span> <strong>${currencySymbol}${c}</strong></div>
            ${lineData.y ? `<div class="mt-1 flex justify-between gap-4 text-purple-600"><span>추세선 (SMA 5):</span> <strong>${currencySymbol}${lineData.y}</strong></div>` : ''}
          </div>
        `;
      }
    },
    plotOptions: {
      candlestick: {
        colors: { upward: '#ef4444', downward: '#3b82f6' },
        wick: { useDataColors: true }
      }
    },
    grid: { borderColor: '#f1f5f9', strokeDashArray: 4 }
  };

  return (
    <div className="bg-white p-6 rounded-2xl border border-slate-100 mt-4 shadow-sm">
      <Chart options={options as any} series={chartData} type="candlestick" height={280} />
    </div>
  );
}
