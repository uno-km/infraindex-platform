"use client";

import React, { useState } from 'react';
import dynamic from 'next/dynamic';
import { Activity } from 'lucide-react';
import BaseChartLayout from './BaseChartLayout';

// apexcharts must be imported dynamically in Next.js to avoid SSR issues
const Chart = dynamic(() => import('react-apexcharts'), { ssr: false });

interface CandlestickChartWidgetProps {
  title: string;
  data: any[]; // OHLC 데이터 배열
  timeframe: string;
  onTimeframeChange: (val: string) => void;
  loading?: boolean;
}

export default function CandlestickChartWidget({
  title,
  data,
  timeframe,
  onTimeframeChange,
  loading = false,
}: CandlestickChartWidgetProps) {
  
  const options: any = {
    chart: {
      type: 'candlestick',
      toolbar: { show: false },
      background: 'transparent',
      animations: { enabled: false }, // avoid flickering on data update
    },
    xaxis: {
      type: 'datetime',
      labels: {
        style: { colors: '#64748b', fontWeight: 600 },
        datetimeUTC: false,
      },
      axisBorder: { show: false },
      axisTicks: { show: false },
    },
    yaxis: {
      labels: {
        formatter: (val: number) => {
          if (val > 1000000) return (val / 10000).toFixed(0) + '만';
          if (val > 10000) return (val / 10000).toFixed(1) + '만';
          return val.toLocaleString();
        },
        style: { colors: '#64748b', fontWeight: 600 }
      },
    },
    grid: {
      borderColor: '#f1f5f9',
      strokeDashArray: 4,
    },
    plotOptions: {
      candlestick: {
        colors: {
          upward: '#ef4444', // 붉은색 (상승)
          downward: '#3b82f6' // 푸른색 (하락)
        },
        wick: {
          useFillColor: true
        }
      }
    },
    tooltip: {
      theme: 'light',
      y: {
        formatter: (val: number) => `₩${val.toLocaleString()}`
      }
    }
  };

  const isEmpty = !data || data.length === 0;

  const rightElement = (
    <select 
      value={timeframe}
      onChange={(e) => onTimeframeChange(e.target.value)}
      className="bg-slate-50 border border-slate-200 text-slate-700 text-sm font-bold rounded-lg px-3 py-1.5 focus:outline-none focus:border-indigo-500 cursor-pointer"
    >
      <option value="1W">1주일</option>
      <option value="1M">1개월</option>
      <option value="3M">3개월</option>
      <option value="1Y">1년</option>
    </select>
  );

  return (
    <BaseChartLayout
      title={title}
      icon={<Activity className="text-emerald-500" size={20} />}
      loading={loading}
      empty={isEmpty && !loading}
      emptyMessage="표시할 시세 동향 데이터가 없습니다."
      rightHeaderElement={rightElement}
    >
      {/* 내부 차트 (ApexCharts) */}
      {!isEmpty && (
        <Chart 
          options={options} 
          series={[{ data }]} 
          type="candlestick" 
          height="100%" 
          width="100%" 
        />
      )}
    </BaseChartLayout>
  );
}
