"use client";

import React, { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
import { 
  Server, Cpu, HardDrive, ShoppingCart, TrendingDown, 
  ExternalLink, CheckCircle2, ChevronRight, Activity 
} from 'lucide-react';

const Chart = dynamic(() => import('react-apexcharts'), { ssr: false });

export function RetailDashboard() {
  const [data, setData] = useState<any[]>([]);
  const [vendors, setVendors] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [products, setProducts] = useState<any[]>([]);
  const [selectedProductId, setSelectedProductId] = useState<string>("");
  const [timeframe, setTimeframe] = useState("1M");
  const [category, setCategory] = useState("GPU");

  // Fetch available products based on category
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const res = await fetch(`/api/v1/market/products?category=${category}`);
        if (res.ok) {
          const data = await res.json();
          setProducts(data);
          if (data.length > 0) {
            setSelectedProductId(data[0].id);
          } else {
            setSelectedProductId("");
          }
        }
      } catch (e) {
        console.error("Failed to fetch products", e);
      }
    };
    fetchProducts();
  }, [category]);

  // Fetch chart data and vendor data for the selected product
  useEffect(() => {
    if (!selectedProductId) {
      setData([]);
      setVendors([]);
      setLoading(false);
      return;
    }
    
    const fetchPricesAndVendors = async () => {
      setLoading(true);
      try {
        // Fetch Historical Prices (OHLC)
        const url = `/api/v1/market/products/${selectedProductId}/prices?period=${timeframe}`;
        const res = await fetch(url).catch(() => null);
        let result = [];
        if (res && res.ok) {
          result = await res.json();
        }

        const candlestickData = result.map((item: any) => ({
          x: new Date(item.time),
          y: [item.open, item.high, item.low, item.close]
        }));
        const minData = result.map((item: any) => ({
          x: new Date(item.time),
          y: item.low
        }));
        const maxData = result.map((item: any) => ({
          x: new Date(item.time),
          y: item.high
        }));
        
        setData([
          { name: '시세 범위', type: 'candlestick', data: candlestickData },
          { name: '최저가 추세', type: 'line', data: minData },
          { name: '최고가 추세', type: 'line', data: maxData }
        ]);

        // Fetch Vendor Comparison
        const vendorUrl = `/api/v1/market/products/${selectedProductId}/vendors`;
        const vRes = await fetch(vendorUrl).catch(() => null);
        if (vRes && vRes.ok) {
          const vData = await vRes.json();
          setVendors(vData);
        } else {
          setVendors([]);
        }

      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    
    fetchPricesAndVendors();
  }, [selectedProductId, timeframe]);

  const selectedProduct = products.find(p => p.id === selectedProductId);
  const lowestVendor = vendors.find(v => v.is_lowest) || vendors[0];

  const formatPrice = (value: number) => {
    return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW' }).format(value);
  };

  const options: any = {
    chart: { type: 'line', height: 350, background: 'transparent', toolbar: { show: false } },
    title: { text: `기간별 시세 동향`, align: 'left', style: { color: '#1e293b', fontWeight: 'bold' } },
    xaxis: { type: 'datetime', labels: { style: { colors: '#64748b' } } },
    yaxis: {
      tooltip: { enabled: true },
      labels: { style: { colors: '#64748b' }, formatter: (val: number) => formatPrice(val) }
    },
    grid: { borderColor: '#f1f5f9', strokeDashArray: 4 },
    theme: { mode: 'light' },
    stroke: { width: [1, 2, 2], curve: 'smooth' },
    colors: ['#000000', '#3b82f6', '#ef4444'],
    plotOptions: { candlestick: { colors: { upward: '#ef4444', downward: '#3b82f6' } } }
  };

  const getProductIcon = (cat: string) => {
    switch(cat?.toUpperCase()) {
      case 'CPU': return <Cpu className="w-16 h-16 text-indigo-500" />;
      case 'RAM': return <HardDrive className="w-16 h-16 text-emerald-500" />;
      case 'SSD': return <HardDrive className="w-16 h-16 text-amber-500" />;
      default: return <Server className="w-16 h-16 text-blue-500" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Search & Filter Header */}
      <div className="bg-white border border-slate-200/60 rounded-2xl p-4 shadow-sm flex flex-col md:flex-row justify-between items-center gap-4">
        <div className="flex bg-slate-100 p-1 rounded-xl">
          {['GPU', 'Server GPU', 'CPU', 'RAM', 'SSD'].map(cat => (
            <button
              key={cat}
              onClick={() => setCategory(cat)}
              className={`px-4 py-2 rounded-lg text-sm font-bold transition-all ${
                category === cat 
                  ? 'bg-white text-indigo-700 shadow-sm' 
                  : 'text-slate-500 hover:text-slate-700'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
        <div className="w-full md:w-auto min-w-[300px]">
          <select 
            value={selectedProductId}
            onChange={(e) => setSelectedProductId(e.target.value)}
            className="w-full bg-slate-50 border border-slate-200 text-slate-800 font-bold rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 appearance-none cursor-pointer"
          >
            {products.length === 0 && <option value="">상품 없음</option>}
            {products.map(p => (
              <option key={p.id} value={p.id}>{p.manufacturer} {p.model_name}</option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-[500px] bg-white rounded-3xl border border-slate-200/60 shadow-sm">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>
      ) : selectedProduct ? (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          
          {/* Left Column: Product Hero */}
          <div className="lg:col-span-4 bg-white border border-slate-200/60 rounded-3xl p-6 shadow-[0_8px_30px_rgb(0,0,0,0.04)] flex flex-col">
            <div className="bg-gradient-to-br from-slate-50 to-slate-100 rounded-2xl aspect-square flex items-center justify-center mb-6 border border-slate-200/50 shadow-inner">
              {getProductIcon(selectedProduct.category)}
            </div>
            <div className="flex-1">
              <div className="text-xs font-black text-indigo-600 tracking-wider uppercase mb-1">
                {selectedProduct.manufacturer}
              </div>
              <h2 className="text-2xl font-black text-slate-800 mb-4 leading-tight">
                {selectedProduct.model_name}
              </h2>
              
              <div className="flex flex-wrap gap-2 mb-6">
                {selectedProduct.generation && (
                  <span className="px-3 py-1 bg-slate-100 text-slate-600 rounded-lg text-xs font-bold border border-slate-200">
                    {selectedProduct.generation}
                  </span>
                )}
                {selectedProduct.vram_gb && (
                  <span className="px-3 py-1 bg-blue-50 text-blue-700 rounded-lg text-xs font-bold border border-blue-100">
                    {selectedProduct.vram_gb}GB VRAM
                  </span>
                )}
                {selectedProduct.memory_type && (
                  <span className="px-3 py-1 bg-emerald-50 text-emerald-700 rounded-lg text-xs font-bold border border-emerald-100">
                    {selectedProduct.memory_type}
                  </span>
                )}
              </div>

              {lowestVendor && (
                <div className="bg-indigo-50 border border-indigo-100 rounded-2xl p-5 mb-4">
                  <div className="flex items-center gap-2 text-indigo-600 text-sm font-bold mb-1">
                    <TrendingDown size={16} /> 최저가
                  </div>
                  <div className="text-3xl font-black text-indigo-900 mb-1">
                    {formatPrice(lowestVendor.total_price)}
                  </div>
                  <div className="text-sm text-indigo-600/80 font-medium flex justify-between items-center">
                    <span>{lowestVendor.vendor_name} 기준</span>
                    <span className="text-xs bg-indigo-200 text-indigo-800 px-2 py-0.5 rounded">배송비 포함</span>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Right Column: Comparison & Chart */}
          <div className="lg:col-span-8 flex flex-col gap-6">
            
            {/* Vendor Comparison List */}
            <div className="bg-white border border-slate-200/60 rounded-3xl p-6 shadow-[0_8px_30px_rgb(0,0,0,0.04)]">
              <h3 className="text-lg font-black text-slate-800 mb-4 flex items-center gap-2">
                <ShoppingCart className="text-indigo-500" size={20} /> 판매처별 가격 비교
              </h3>
              
              <div className="space-y-3 overflow-y-auto max-h-[300px] pr-2 custom-scrollbar">
                {vendors.map((vendor, idx) => (
                  <div 
                    key={idx} 
                    className={`flex items-center justify-between p-4 rounded-2xl border transition-all hover:shadow-md ${
                      vendor.is_lowest 
                        ? 'border-indigo-500 bg-indigo-50/30' 
                        : 'border-slate-200 bg-white hover:border-slate-300'
                    }`}
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center font-bold text-slate-500 text-sm">
                        {vendor.vendor_name.substring(0,1)}
                      </div>
                      <div>
                        <div className="font-bold text-slate-800 flex items-center gap-2">
                          {vendor.vendor_name}
                          {vendor.is_lowest && (
                            <span className="bg-red-500 text-white text-[10px] font-black px-2 py-0.5 rounded-full">최저가</span>
                          )}
                        </div>
                        <div className="text-xs text-slate-500 mt-0.5 flex gap-2">
                          <span className="flex items-center gap-1"><CheckCircle2 size={12}/> {vendor.condition === 'new' ? '새상품' : '중고'}</span>
                          <span>|</span>
                          <span>배송비 {vendor.shipping_fee === 0 ? '무료' : formatPrice(vendor.shipping_fee)}</span>
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center gap-6">
                      <div className="text-right">
                        <div className="text-xl font-black text-slate-900">{formatPrice(vendor.total_price)}</div>
                      </div>
                      <a 
                        href={vendor.url} 
                        target="_blank" 
                        rel="noreferrer"
                        className={`flex items-center justify-center w-10 h-10 rounded-xl transition-colors ${
                          vendor.is_lowest 
                            ? 'bg-indigo-600 text-white hover:bg-indigo-700' 
                            : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                        }`}
                      >
                        <ExternalLink size={18} strokeWidth={2.5} />
                      </a>
                    </div>
                  </div>
                ))}
                {vendors.length === 0 && (
                  <div className="text-center py-8 text-slate-400 font-medium">
                    등록된 판매처 정보가 없습니다.
                  </div>
                )}
              </div>
            </div>

            {/* Price Trend Chart */}
            <div className="bg-white border border-slate-200/60 rounded-3xl p-6 shadow-[0_8px_30px_rgb(0,0,0,0.04)]">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-black text-slate-800 flex items-center gap-2">
                  <Activity className="text-emerald-500" size={20} /> 시세 동향 차트
                </h3>
                <select 
                  value={timeframe}
                  onChange={(e) => setTimeframe(e.target.value)}
                  className="bg-slate-50 border border-slate-200 text-slate-700 text-sm font-bold rounded-lg px-3 py-1.5 focus:outline-none focus:border-indigo-500"
                >
                  <option value="1W">1주일</option>
                  <option value="1M">1개월</option>
                  <option value="3M">3개월</option>
                  <option value="1Y">1년</option>
                </select>
              </div>
              <div className="w-full text-slate-800 h-[350px]">
                <Chart options={options} series={data} type="candlestick" height="100%" width="100%" />
              </div>
            </div>

          </div>
        </div>
      ) : (
        <div className="flex justify-center items-center h-[500px] bg-white rounded-3xl border border-slate-200/60 shadow-sm text-slate-400 font-bold">
          선택된 상품이 없거나 데이터를 불러올 수 없습니다.
        </div>
      )}
    </div>
  );
}
