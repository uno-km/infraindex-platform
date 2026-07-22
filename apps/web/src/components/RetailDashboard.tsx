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
        color: '#fff'
      }
    },
    xaxis: {
      type: 'datetime',
      labels: {
        style: {
          colors: '#a1a1aa' // zinc-400
        }
      }
    },
    yaxis: {
      tooltip: {
        enabled: true
      },
      labels: {
        style: {
          colors: '#a1a1aa' // zinc-400
        },
        formatter: (value: number) => {
          return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW' }).format(value);
        }
      }
    },
    grid: {
      borderColor: '#3f3f46' // zinc-700
    },
    theme: {
      mode: 'dark'
    }
  };

  return (
    <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6 w-full mt-8 shadow-xl">
      <div className="flex flex-col md:flex-row justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-white flex items-center gap-3">
          <span className="bg-gradient-to-r from-blue-500 to-cyan-400 text-transparent bg-clip-text">Retail Market</span>
          <span className="text-zinc-500 font-normal">|</span>
          <span className="text-lg text-zinc-300">Price History</span>
        </h2>
        
        <div className="flex gap-4 mt-4 md:mt-0">
          <select 
            value={hardwareType}
            onChange={(e) => setHardwareType(e.target.value)}
            className="bg-zinc-800 border border-zinc-700 text-white rounded-md px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="gpu">GPU</option>
            <option value="cpu">CPU</option>
            <option value="ram">RAM</option>
          </select>
          
          <select 
            value={timeframe}
            onChange={(e) => setTimeframe(e.target.value)}
            className="bg-zinc-800 border border-zinc-700 text-white rounded-md px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500"
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
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
        </div>
      ) : (
        <div className="w-full text-black">
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
