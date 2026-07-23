"use client";

import React, { useEffect, useState, useCallback } from 'react';
import dynamic from 'next/dynamic';
import { TrendingUp, TrendingDown, Minus, ShoppingBag, RefreshCw } from 'lucide-react';
import BaseChartLayout from '@/components/chart/BaseChartLayout';

const Chart = dynamic(() => import('react-apexcharts'), { ssr: false });

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://127.0.0.1:8000/api/v1';

interface Product {
  id: string;
  manufacturer: string;
  model_name: string;
  category: string;
  product_line: string | null;
}

interface OHLCPoint {
  x: string;
  o: number;
  h: number;
  l: number;
  c: number;
}

interface Summary {
  current_price: number | null;
  change_1d: number | null;
  change_pct_1d: number | null;
  all_time_high: number | null;
  all_time_low: number | null;
  data_points: number;
}

const TIMEFRAMES = ['1W', '1M', '3M', '1Y'] as const;
type Timeframe = typeof TIMEFRAMES[number];

function formatKRW(val: number): string {
  if (val >= 100_000_000) return `${(val / 100_000_000).toFixed(1)}억원`;
  if (val >= 10_000) return `${(val / 10_000).toFixed(0)}만원`;
  return `₩${val.toLocaleString('ko-KR')}`;
}

export default function RetailChartPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [timeframe, setTimeframe] = useState<Timeframe>('1M');
  const [ohlcData, setOhlcData] = useState<OHLCPoint[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(false);
  const [category, setCategory] = useState<string>('');

  // 상품 목록 로드
  useEffect(() => {
    async function loadProducts() {
      try {
        const res = await fetch(
          `${API_BASE}/retail/chart/products${category ? `?category=${category}` : ''}`
        );
        const data = await res.json();
        setProducts(data);
        if (data.length > 0 && !selectedProduct) {
          setSelectedProduct(data[0]);
        }
      } catch (e) {
        console.error('Failed to load products', e);
      }
    }
    loadProducts();
  }, [category]);

  // OHLC + 요약 로드
  const loadChartData = useCallback(async () => {
    if (!selectedProduct) return;
    setLoading(true);
    try {
      const [ohlcRes, summaryRes] = await Promise.all([
        fetch(`${API_BASE}/retail/chart/ohlc?product_id=${selectedProduct.id}&timeframe=${timeframe}`),
        fetch(`${API_BASE}/retail/chart/summary?product_id=${selectedProduct.id}`),
      ]);
      const ohlc = await ohlcRes.json();
      const sum = await summaryRes.json();
      setOhlcData(ohlc);
      setSummary(sum);
    } catch (e) {
      console.error('Failed to load chart data', e);
    } finally {
      setLoading(false);
    }
  }, [selectedProduct, timeframe]);

  useEffect(() => {
    loadChartData();
  }, [loadChartData]);

  const chartOptions: any = {
    chart: {
      type: 'candlestick',
      toolbar: { show: false },
      background: 'transparent',
      animations: { enabled: true, speed: 400 },
    },
    xaxis: {
      type: 'datetime',
      labels: {
        style: { colors: '#64748b', fontWeight: 600, fontSize: '12px' },
        datetimeUTC: false,
      },
      axisBorder: { show: false },
      axisTicks: { show: false },
    },
    yaxis: {
      labels: {
        formatter: (val: number) => formatKRW(val),
        style: { colors: '#64748b', fontWeight: 600, fontSize: '12px' },
      },
    },
    grid: { borderColor: '#f1f5f9', strokeDashArray: 4 },
    plotOptions: {
      candlestick: {
        colors: { upward: '#ef4444', downward: '#3b82f6' },
        wick: { useFillColor: true },
      },
    },
    tooltip: {
      theme: 'light',
      y: { formatter: (val: number) => formatKRW(val) },
    },
  };

  const change = summary?.change_pct_1d ?? 0;
  const isUp = change > 0;
  const isDown = change < 0;

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* 헤더 */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-black text-slate-900 flex items-center gap-3">
            <ShoppingBag className="text-emerald-500" size={32} />
            리테일 시장 가격 차트
          </h1>
          <p className="text-slate-500 font-medium mt-1 ml-11">
            네이버 쇼핑 · 쿠팡 파트너스 실시간 가격 추이
          </p>
        </div>
        <button
          onClick={loadChartData}
          disabled={loading}
          className="flex items-center gap-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold px-4 py-2 rounded-xl transition-all"
        >
          <RefreshCw size={16} className={loading ? 'animate-spin' : ''} />
          새로고침
        </button>
      </div>

      <div className="flex gap-6">
        {/* 사이드 — 상품 목록 */}
        <div className="w-72 shrink-0">
          {/* 카테고리 필터 */}
          <div className="flex gap-2 mb-3">
            {['', 'GPU', 'CPU'].map((cat) => (
              <button
                key={cat}
                onClick={() => setCategory(cat)}
                className={`px-3 py-1.5 rounded-lg text-sm font-bold transition-all ${
                  category === cat
                    ? 'bg-indigo-600 text-white shadow'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {cat || '전체'}
              </button>
            ))}
          </div>

          {/* 상품 리스트 */}
          <div className="flex flex-col gap-2 max-h-[600px] overflow-y-auto pr-1">
            {products.length === 0 && (
              <div className="text-slate-400 text-sm text-center py-8 border-2 border-dashed border-slate-200 rounded-xl">
                집계된 상품이 없습니다.
                <br />
                크롤러를 먼저 실행해주세요.
              </div>
            )}
            {products.map((p) => (
              <button
                key={p.id}
                onClick={() => setSelectedProduct(p)}
                className={`text-left p-3 rounded-xl border-2 transition-all ${
                  selectedProduct?.id === p.id
                    ? 'border-indigo-500 bg-indigo-50 shadow-md'
                    : 'border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50'
                }`}
              >
                <p className="font-black text-slate-800 text-sm">{p.model_name}</p>
                <p className="text-slate-500 text-xs mt-0.5">
                  {p.manufacturer} · {p.category}
                </p>
              </button>
            ))}
          </div>
        </div>

        {/* 메인 — 차트 영역 */}
        <div className="flex-1 flex flex-col gap-4">
          {/* 요약 카드 */}
          {selectedProduct && summary && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div className="bg-white border border-slate-200/60 rounded-2xl p-4 shadow-sm">
                <p className="text-xs font-bold text-slate-400 uppercase tracking-wide">현재가</p>
                <p className="text-2xl font-black text-slate-900 mt-1">
                  {summary.current_price ? formatKRW(summary.current_price) : '-'}
                </p>
              </div>
              <div className="bg-white border border-slate-200/60 rounded-2xl p-4 shadow-sm">
                <p className="text-xs font-bold text-slate-400 uppercase tracking-wide">전일 대비</p>
                <p className={`text-2xl font-black mt-1 flex items-center gap-1 ${isUp ? 'text-red-500' : isDown ? 'text-blue-500' : 'text-slate-500'}`}>
                  {isUp ? <TrendingUp size={20} /> : isDown ? <TrendingDown size={20} /> : <Minus size={20} />}
                  {summary.change_pct_1d !== null ? `${Math.abs(summary.change_pct_1d).toFixed(2)}%` : '-'}
                </p>
              </div>
              <div className="bg-white border border-slate-200/60 rounded-2xl p-4 shadow-sm">
                <p className="text-xs font-bold text-slate-400 uppercase tracking-wide">역대 최고</p>
                <p className="text-2xl font-black text-red-500 mt-1">
                  {summary.all_time_high ? formatKRW(summary.all_time_high) : '-'}
                </p>
              </div>
              <div className="bg-white border border-slate-200/60 rounded-2xl p-4 shadow-sm">
                <p className="text-xs font-bold text-slate-400 uppercase tracking-wide">역대 최저</p>
                <p className="text-2xl font-black text-blue-500 mt-1">
                  {summary.all_time_low ? formatKRW(summary.all_time_low) : '-'}
                </p>
              </div>
            </div>
          )}

          {/* 캔들스틱 차트 */}
          <BaseChartLayout
            title={selectedProduct ? `${selectedProduct.manufacturer} ${selectedProduct.model_name} 가격 추이` : '상품을 선택하세요'}
            icon={<ShoppingBag className="text-emerald-500" size={20} />}
            description={`기간: ${TIMEFRAMES.find(t => t === timeframe)} | 출처: Naver Shopping + Coupang`}
            loading={loading}
            empty={!loading && ohlcData.length === 0}
            emptyMessage="아직 집계된 가격 데이터가 없습니다. 크롤러를 실행하거나 내일 다시 확인해주세요."
            rightHeaderElement={
              <div className="flex gap-1.5">
                {TIMEFRAMES.map((tf) => (
                  <button
                    key={tf}
                    onClick={() => setTimeframe(tf)}
                    className={`px-3 py-1.5 rounded-lg text-sm font-bold transition-all ${
                      timeframe === tf
                        ? 'bg-indigo-600 text-white shadow'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    }`}
                  >
                    {tf}
                  </button>
                ))}
              </div>
            }
          >
            {ohlcData.length > 0 && (
              <Chart
                options={chartOptions}
                series={[{ data: ohlcData.map(d => ({ x: new Date(d.x).getTime(), y: [d.o, d.h, d.l, d.c] })) }]}
                type="candlestick"
                height="100%"
                width="100%"
              />
            )}
          </BaseChartLayout>
        </div>
      </div>
    </div>
  );
}
