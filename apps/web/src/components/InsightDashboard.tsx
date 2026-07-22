"use client";

import React, { useEffect, useState } from "react";
import dynamic from "next/dynamic";

const Chart = dynamic(() => import("react-apexcharts"), { ssr: false });

export default function InsightDashboard() {
  const [data, setData] = useState<any[]>([]);
  const [timeframe, setTimeframe] = useState("1mo");

  useEffect(() => {
    fetch(`/api/v1/insights/correlation?timeframe=${timeframe}`)
      .then((res) => res.json())
      .then((json) => {
        if (Array.isArray(json)) {
          setData(json);
        }
      })
      .catch((err) => console.error("Failed to fetch insights:", err));
  }, [timeframe]);

  // For a correlation chart, we ideally plot time series. 
  // However, the current API returns a summary of start vs end percentage change.
  // A bar chart is perfect to show the relative performance (percentage change) over the timeframe.
  
  const categories = data.map((d) => d.asset);
  const seriesData = data.map((d) => d.percentage_change);
  
  const chartOptions = {
    chart: {
      type: "bar" as const,
      background: "transparent",
      toolbar: { show: false }
    },
    theme: { mode: "dark" as const },
    colors: [
      function({ value }: { value: number }) {
        if (value < 0) return '#ef4444'; // red for negative
        return '#22c55e'; // green for positive
      }
    ],
    plotOptions: {
      bar: {
        horizontal: true,
        borderRadius: 4,
        dataLabels: {
          position: "top"
        }
      }
    },
    dataLabels: {
      enabled: true,
      formatter: (val: number) => `${val}%`,
      style: {
        colors: ["#fff"]
      }
    },
    xaxis: {
      categories: categories,
      title: { text: "Percentage Change (%)" },
      labels: {
        style: { colors: "#9ca3af" }
      }
    },
    yaxis: {
      labels: {
        style: { colors: "#e5e7eb", fontSize: "13px", fontWeight: 600 }
      }
    },
    tooltip: {
      y: {
        formatter: (val: number) => `${val}%`
      }
    }
  };

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 shadow-2xl">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-indigo-500">
            Market Correlation Insights
          </h2>
          <p className="text-gray-400 text-sm mt-1">
            Compare GPU pricing trends with Semiconductor Stocks & Futures
          </p>
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

      <div className="h-[400px]">
        {data.length > 0 ? (
          <Chart options={chartOptions} series={[{ name: "Performance", data: seriesData }]} type="bar" height="100%" />
        ) : (
          <div className="flex items-center justify-center h-full text-gray-500">
            Loading market insights...
          </div>
        )}
      </div>
    </div>
  );
}
