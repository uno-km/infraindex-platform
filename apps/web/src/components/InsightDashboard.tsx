"use client";

import React, { useEffect, useState } from "react";
import dynamic from "next/dynamic";

const Chart = dynamic(() => import("react-apexcharts"), { ssr: false });

export default function InsightDashboard() {
  const [data, setData] = useState<any[]>([]);
  const [timeframe, setTimeframe] = useState("1mo");
  const [chartType, setChartType] = useState<"bar" | "scatter">("bar");

  useEffect(() => {
    fetch(`/api/v1/insights/correlation?timeframe=${timeframe}`)
      .then((res) => {
        if (!res.ok) throw new Error("API_ERROR");
        return res.json();
      })
      .then((json) => {
        if (Array.isArray(json)) {
          setData(json);
        }
      })
      .catch((err) => {
        console.error("Insights API failed:", err);
        setData([]);
      });
  }, [timeframe]);

  // --- Data Processing for Bar Chart (Top 15) ---
  const sortedData = [...data].sort((a, b) => Math.abs(b.percentage_change) - Math.abs(a.percentage_change));
  const top15Data = sortedData.slice(0, 15);
  
  const chartOptionsBar = {
    chart: { type: "bar", background: "transparent", toolbar: { show: false } },
    theme: { mode: "dark" },
    colors: [
      function({ value, dataPointIndex }: any) {
        const realValue = top15Data[dataPointIndex]?.percentage_change || value;
        return realValue < 0 ? '#ef4444' : '#22c55e';
      }
    ],
    plotOptions: { bar: { horizontal: true, borderRadius: 4, dataLabels: { position: "top" } } },
    dataLabels: {
      enabled: true,
      formatter: function(val: number, opts: any) {
        const realValue = top15Data[opts.dataPointIndex]?.percentage_change;
        const disp = realValue !== undefined ? realValue : val;
        if (disp > 200) return `🔥 ${disp}%`;
        if (disp < -200) return `🧊 ${disp}%`;
        return `${disp}%`;
      },
      style: { colors: ["#fff"] }
    },
    xaxis: {
      categories: top15Data.map(d => d.asset),
      title: { text: "Percentage Change (%)" },
      labels: { style: { colors: "#9ca3af" } },
      min: -200, 
      max: 200
    },
    yaxis: { labels: { style: { colors: "#e5e7eb", fontSize: "12px", fontWeight: 600 } } },
    tooltip: {
      y: {
        formatter: function(val: number, opts: any) {
           const realValue = top15Data[opts.dataPointIndex]?.percentage_change;
           return `${realValue !== undefined ? realValue : val}%`;
        }
      }
    }
  };

  const seriesBar = [{ name: "Performance", data: top15Data.map(d => Math.max(-200, Math.min(200, d.percentage_change))) }];

  // --- Data Processing for Scatter Plot (All Data) ---
  const chartOptionsScatter = {
    chart: { type: "scatter", background: "transparent", toolbar: { show: true }, zoom: { enabled: true, type: 'xy' } },
    theme: { mode: "dark" },
    colors: ['#06b6d4'], // Cyan
    xaxis: {
      type: 'category',
      categories: data.map(d => d.asset),
      labels: { show: false }, // Hide labels to prevent overlap
      title: { text: "Assets (Hover points for name)" }
    },
    yaxis: {
      title: { text: "Percentage Change (%)" },
      labels: { style: { colors: "#9ca3af" } }
    },
    tooltip: {
      custom: function({series, seriesIndex, dataPointIndex, w}: any) {
        const item = data[dataPointIndex];
        if(!item) return '';
        const color = item.percentage_change >= 0 ? '#22c55e' : '#ef4444';
        return `
          <div style="background: #1f2937; border: 1px solid #374151; padding: 10px; border-radius: 8px;">
            <div style="color: #fff; font-weight: bold; margin-bottom: 5px;">${item.asset}</div>
            <div style="color: ${color};">${item.percentage_change}%</div>
          </div>
        `;
      }
    }
  };

  const seriesScatter = [{
    name: "Volatility",
    data: data.map(d => d.percentage_change)
  }];

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-2xl">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4">
        <div>
          <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-indigo-500">
            Market Correlation Insights
          </h2>
          <p className="text-gray-400 text-sm mt-1">
            Compare GPU pricing trends with Semiconductor Stocks & Futures
          </p>
        </div>
        
        <div className="flex gap-4 items-center">
          <div className="flex bg-gray-800 rounded-lg p-1 border border-gray-700">
            <button 
              className={`px-4 py-1.5 text-sm rounded-md transition-colors ${chartType === 'bar' ? 'bg-gray-700 text-white shadow' : 'text-gray-400 hover:text-gray-200'}`}
              onClick={() => setChartType('bar')}
            >
              Top 15 Bar
            </button>
            <button 
              className={`px-4 py-1.5 text-sm rounded-md transition-colors ${chartType === 'scatter' ? 'bg-gray-700 text-white shadow' : 'text-gray-400 hover:text-gray-200'}`}
              onClick={() => setChartType('scatter')}
            >
              Scatter Plot
            </button>
          </div>

          <select 
            className="bg-gray-800 border border-gray-700 text-white text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2"
            value={timeframe}
            onChange={(e) => setTimeframe(e.target.value)}
          >
            <option value="1w">1 Week</option>
            <option value="1mo">1 Month</option>
            <option value="3mo">3 Months</option>
          </select>
        </div>
      </div>

      <div className="h-[500px]">
        {data.length > 0 ? (
          chartType === 'bar' ? (
            <Chart options={chartOptionsBar as any} series={seriesBar} type="bar" height="100%" />
          ) : (
             <Chart options={chartOptionsScatter as any} series={seriesScatter} type="scatter" height="100%" />
          )
        ) : (
          <div className="flex items-center justify-center h-full text-gray-500">
            Loading market insights...
          </div>
        )}
      </div>
    </div>
  );
}
