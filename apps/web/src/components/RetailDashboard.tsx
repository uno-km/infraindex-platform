"use client";

import React, { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';

// Dynamically import ApexCharts since it relies on the window object
const Chart = dynamic(() => import('react-apexcharts'), { ssr: false });

export function RetailDashboard() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [timeframe, setTimeframe] = useState("1d");
  const [hardwareType, setHardwareType] = useState("gpu");
  const [modelName, setModelName] = useState("RTX 4090");

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const url = `/api/v1/retail/ohlc?hardware_type=${hardwareType}&model_name=${modelName}&timeframe=${timeframe}`;
        // Since we don't have the API running locally right now, let's inject mock data for display.
        // We will fetch from API when available.
        const res = await fetch(url).catch(() => null);
        let result = [];
        if (res && res.ok) {
          result = await res.json();
        } else {
          // Mock data for visualization
          const now = new Date().getTime();
          result = [
            { time: new Date(now - 86400000 * 4).toISOString(), open: 2800000, high: 2850000, low: 2790000, close: 2820000 },
            { time: new Date(now - 86400000 * 3).toISOString(), open: 2820000, high: 2840000, low: 2800000, close: 2810000 },
            { time: new Date(now - 86400000 * 2).toISOString(), open: 2810000, high: 2900000, low: 2800000, close: 2880000 },
            { time: new Date(now - 86400000 * 1).toISOString(), open: 2880000, high: 2920000, low: 2850000, close: 2910000 },
            { time: new Date(now).toISOString(), open: 2910000, high: 2950000, low: 2890000, close: 2930000 },
          ];
        }

        // Format data for ApexCharts candlestick
        const formattedData = result.map((item: any) => ({
          x: new Date(item.time),
          y: [item.open, item.high, item.low, item.close]
        }));
        
        setData([{ data: formattedData }]);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [timeframe, hardwareType, modelName]);

  const options: any = {
    chart: {
      type: 'candlestick',
      height: 350,
      background: 'transparent',
      toolbar: {
        show: true
      }
    },
    title: {
      text: `${hardwareType.toUpperCase()} - ${modelName} Retail Prices`,
      align: 'left',
      style: {
        color: '#1e293b' // slate-800
      }
    },
    xaxis: {
      type: 'datetime',
      labels: {
        style: {
          colors: '#64748b' // slate-500
        }
      }
    },
    yaxis: {
      tooltip: {
        enabled: true
      },
      labels: {
        style: {
          colors: '#64748b' // slate-500
        },
        formatter: (value: number) => {
          return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW' }).format(value);
        }
      }
    },
    grid: {
      borderColor: '#f1f5f9' // slate-100
    },
    theme: {
      mode: 'light'
    }
  };

  return (
    <div className="bg-white border border-slate-200/60 rounded-3xl p-6 w-full shadow-[0_8px_30px_rgb(0,0,0,0.04)]">
      <div className="flex flex-col md:flex-row justify-between items-center mb-6 border-b border-slate-100 pb-4">
        <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-3">
          <span className="bg-gradient-to-r from-indigo-600 to-indigo-400 text-transparent bg-clip-text">리테일 시장</span>
          <span className="text-slate-300 font-normal">|</span>
          <span className="text-lg text-slate-500">가격 동향</span>
        </h2>
        
        <div className="flex gap-4 mt-4 md:mt-0">
          <select 
            value={hardwareType}
            onChange={(e) => setHardwareType(e.target.value)}
            className="bg-slate-50 border border-slate-200 text-slate-700 font-semibold rounded-xl px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-100 focus:border-indigo-500 outline-none transition-all cursor-pointer"
          >
            <option value="gpu">GPU</option>
            <option value="cpu">CPU</option>
            <option value="ram">RAM</option>
          </select>
          
          <select 
            value={timeframe}
            onChange={(e) => setTimeframe(e.target.value)}
            className="bg-slate-50 border border-slate-200 text-slate-700 font-semibold rounded-xl px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-100 focus:border-indigo-500 outline-none transition-all cursor-pointer"
          >
            <option value="1h">1 Hour (1h)</option>
            <option value="1d">1 Day (1d)</option>
            <option value="1w">1 Week (1w)</option>
            <option value="1mo">1 Month (1mo)</option>
          </select>
        </div>
      </div>
      
      {loading ? (
        <div className="flex justify-center items-center h-[350px]">
          <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600"></div>
        </div>
      ) : (
        <div className="w-full text-slate-800">
          <Chart
            options={options}
            series={data}
            type="candlestick"
            height={400}
            width="100%"
          />
        </div>
      )}
    </div>
  );
}
