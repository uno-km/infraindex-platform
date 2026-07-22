"use client";

import { useEffect, useState, useMemo } from "react";
import { Zap, Search, Menu, User, Clock, Heart, ChevronRight, Image as ImageIcon, Filter, TrendingUp } from "lucide-react";
import dynamic from "next/dynamic";

// Dynamically import ApexCharts to prevent SSR issues
const Chart = dynamic(() => import("react-apexcharts"), { ssr: false });

interface Offer {
  provider: string;
  price_per_hour: number;
  is_available: boolean;
  region: string;
  provider_link?: string;
  sys_ram_gb?: number;
  tdp_w?: number;
}

interface GpuModel {
  id: string;
  name: string;
  vram_gb: number;
  offers: Offer[];
}

// --------------------------------------------------------------------------------
// 1. Candlestick Chart Component for Daily Price History
// --------------------------------------------------------------------------------
const GpuCandlestickChart = ({ gpuName, basePrice }: { gpuName: string, basePrice: number }) => {
  // Generate fake daily OHLC data for the last 30 days based on the current price
  // In a real app, this would fetch from /api/v1/history/candles
  const seriesData = useMemo(() => {
    const data = [];
    let currentPrice = basePrice;
    const now = new Date();
    
    for (let i = 30; i >= 0; i--) {
      const date = new Date(now.getTime() - i * 24 * 60 * 60 * 1000);
      const volatility = currentPrice * 0.05; // 5% daily volatility
      const open = currentPrice + (Math.random() - 0.5) * volatility;
      const close = open + (Math.random() - 0.5) * volatility;
      const high = Math.max(open, close) + Math.random() * volatility;
      const low = Math.min(open, close) - Math.random() * volatility;
      
      data.push({
        x: date,
        y: [
          parseFloat(open.toFixed(3)),
          parseFloat(high.toFixed(3)),
          parseFloat(low.toFixed(3)),
          parseFloat(close.toFixed(3))
        ]
      });
      currentPrice = close;
    }
    return [{ data }];
  }, [basePrice]);

  const options = {
    chart: { type: 'candlestick', toolbar: { show: false }, fontFamily: 'inherit' },
    title: { text: `${gpuName} 일일 시세 변동 차트 (30일)`, align: 'left', style: { fontSize: '14px', fontWeight: 'bold' } },
    xaxis: { type: 'datetime', labels: { style: { colors: '#6B7280' } } },
    yaxis: { 
      tooltip: { enabled: true }, 
      labels: { formatter: (val: number) => `$${val.toFixed(2)}` } 
    },
    plotOptions: {
      candlestick: {
        colors: { upward: '#ef4444', downward: '#3b82f6' }, // Red for up, Blue for down (Korean stock style)
        wick: { useDataColors: true }
      }
    },
    grid: { borderColor: '#f1f1f1' }
  };

  return (
    <div className="bg-white p-4 rounded-lg border border-gray-200 mt-4 shadow-inner">
      <Chart options={options as any} series={seriesData} type="candlestick" height={250} />
      <div className="text-xs text-gray-400 text-right mt-1">* 9시, 13시, 18시 수집된 최저가 기준 OHLC 모의 데이터</div>
    </div>
  );
};

// --------------------------------------------------------------------------------
// 2. Main Dashboard Component
// --------------------------------------------------------------------------------
export default function GpuDashboard() {
  const [gpus, setGpus] = useState<GpuModel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  
  // Filters & Sorting
  const [selectedSeries, setSelectedSeries] = useState<string>("ALL");
  const [sortBy, setSortBy] = useState<"PRICE_ASC" | "VRAM_DESC">("PRICE_ASC");
  
  // Chart selection
  const [selectedChartGpu, setSelectedChartGpu] = useState<string | null>(null);

  useEffect(() => {
    async function fetchGpus() {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const res = await fetch(`${apiUrl}/api/v1/gpus`);
        if (!res.ok) throw new Error("Failed to fetch data");
        const data = await res.json();
        setGpus(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchGpus();
  }, []);

  // --- Dynamic Filtering Logic ---
  const seriesOptions = useMemo(() => {
    const seriesSet = new Set<string>();
    gpus.forEach(g => {
      if (g.name.includes("RTX")) seriesSet.add("RTX 시리즈");
      else if (g.name.includes("A100") || g.name.includes("A10") || g.name.includes("A6000")) seriesSet.add("A 시리즈");
      else if (g.name.includes("H100")) seriesSet.add("H 시리즈");
      else if (g.name.includes("L40") || g.name.includes("L4")) seriesSet.add("L 시리즈");
      else if (g.name.includes("V100")) seriesSet.add("V 시리즈");
      else seriesSet.add("기타");
    });
    return ["ALL", ...Array.from(seriesSet)];
  }, [gpus]);

  const filteredAndSortedGpus = useMemo(() => {
    let result = gpus.filter(g => g.name.toLowerCase().includes(searchQuery.toLowerCase()));
    
    if (selectedSeries !== "ALL") {
      result = result.filter(g => {
        if (selectedSeries === "RTX 시리즈") return g.name.includes("RTX");
        if (selectedSeries === "A 시리즈") return g.name.includes("A100") || g.name.includes("A10") || g.name.includes("A6000");
        if (selectedSeries === "H 시리즈") return g.name.includes("H100");
        if (selectedSeries === "L 시리즈") return g.name.includes("L40") || g.name.includes("L4");
        if (selectedSeries === "V 시리즈") return g.name.includes("V100");
        return !g.name.includes("RTX") && !g.name.includes("A100") && !g.name.includes("H100") && !g.name.includes("L40") && !g.name.includes("V100");
      });
    }

    result.sort((a, b) => {
      const minPriceA = Math.min(...a.offers.map(o => o.price_per_hour));
      const minPriceB = Math.min(...b.offers.map(o => o.price_per_hour));
      
      if (sortBy === "PRICE_ASC") return minPriceA - minPriceB;
      if (sortBy === "VRAM_DESC") return b.vram_gb - a.vram_gb;
      return 0;
    });

    return result;
  }, [gpus, searchQuery, selectedSeries, sortBy]);


  // Categories for the sidebar
  const categories = [
    { icon: "⚡", name: "GPU (그래픽카드)", active: true },
    { icon: "🧠", name: "CPU (프로세서)" },
    { icon: "💾", name: "RAM (메모리)" },
    { icon: "☁️", name: "클라우드 인스턴스" },
    { icon: "🖥️", name: "베어메탈 서버" },
    { icon: "📦", name: "스토리지 (블록/오브젝트)" },
    { icon: "🌐", name: "네트워크 (CDN/트래픽)" },
    { icon: "🛠️", name: "소프트웨어 (라이선스)" },
  ];

  if (loading) return <div className="h-screen flex items-center justify-center"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#00b050]"></div></div>;

  return (
    <div className="min-h-screen bg-[#F8F9FA] font-sans text-gray-900 pb-20">
      {/* HEADER */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="bg-gray-100 text-xs text-gray-500 py-1">
          <div className="max-w-[1200px] mx-auto flex justify-end gap-4 px-4">
            <span className="hover:text-gray-900 cursor-pointer">에누리</span>
            <span className="hover:text-gray-900 cursor-pointer">다나와</span>
            <span className="hover:text-gray-900 cursor-pointer">InfraIndex</span>
          </div>
        </div>
        
        <div className="max-w-[1200px] mx-auto flex items-center justify-between py-6 px-4">
          <div className="flex items-center gap-10">
            <div className="text-3xl font-black text-[#00b050] tracking-tighter cursor-pointer flex items-end">
              GPUawa <span className="text-xs text-gray-500 font-normal ml-2 mb-1 tracking-normal">비교하고 잘 사는 GPU와</span>
            </div>
          </div>

          <div className="flex-1 max-w-[500px] mx-10">
            <div className="relative flex items-center">
              <input 
                type="text" 
                placeholder="A100, H100 등 모델명을 검색해보세요" 
                className="w-full border-2 border-[#00b050] rounded-full py-3 px-6 pr-14 text-sm font-medium outline-none focus:ring-2 focus:ring-[#00b050]/20"
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
              />
              <button className="absolute right-4 text-[#00b050]">
                <Search size={24} strokeWidth={2.5} />
              </button>
            </div>
          </div>

          <div className="flex gap-6 items-center">
            <div className="flex flex-col items-center cursor-pointer hover:text-[#00b050] transition-colors">
              <TrendingUp size={28} strokeWidth={1.5} className="text-gray-600 mb-1" />
              <span className="text-xs">시세동향</span>
            </div>
            <div className="flex flex-col items-center cursor-pointer hover:text-[#00b050] transition-colors">
              <Heart size={28} strokeWidth={1.5} className="text-gray-600 mb-1" />
              <span className="text-xs">관심</span>
            </div>
            <div className="flex flex-col items-center cursor-pointer hover:text-[#00b050] transition-colors">
              <User size={28} strokeWidth={1.5} className="text-gray-600 mb-1" />
              <span className="text-xs">로그인</span>
            </div>
          </div>
        </div>
      </header>

      {/* MAIN CONTENT GRID */}
      <div className="max-w-[1200px] mx-auto mt-6 px-4 flex gap-6 items-start">
        
        {/* LEFT SIDEBAR (Category Menu) */}
        <aside className="w-[220px] flex-shrink-0 bg-white border border-gray-200 rounded-lg overflow-hidden shadow-sm sticky top-[140px]">
          <div className="bg-[#00b050] text-white py-4 px-4 flex items-center font-bold text-lg cursor-pointer">
            <Menu className="mr-2" size={20} /> 전체 카테고리
          </div>
          <ul className="py-2">
            {categories.map((cat, idx) => (
              <li key={idx} className={`px-4 py-3 text-sm font-semibold border-b border-gray-50 last:border-0 cursor-pointer flex justify-between items-center transition-colors ${cat.active ? 'bg-gray-50 text-[#00b050]' : 'text-gray-700 hover:bg-gray-50 hover:text-[#00b050]'}`}>
                <span className="flex items-center gap-3">
                  <span className="text-base">{cat.icon}</span>
                  {cat.name}
                </span>
                {cat.active && <ChevronRight size={16} />}
              </li>
            ))}
          </ul>
        </aside>

        {/* CENTER & RIGHT MAIN AREA */}
        <main className="flex-1 min-w-0">
          
          {/* Hero Banner Area */}
          <div className="bg-[#111] rounded-lg overflow-hidden mb-6 relative h-[140px] flex items-center justify-between px-10 cursor-pointer shadow-md">
            <div className="z-10 text-white">
              <div className="text-[#00ff88] font-bold mb-2 flex items-center gap-2">
                <span className="bg-[#00ff88] text-black text-[10px] px-1.5 py-0.5 rounded">HOT</span> 
                매일 9시, 13시, 18시 실시간 시세 업데이트!
              </div>
              <h2 className="text-2xl font-bold">국내외 클라우드 GPU 대여료 한눈에 비교</h2>
            </div>
            <div className="absolute right-0 top-0 h-full w-1/2 bg-gradient-to-l from-black/80 to-transparent z-0"></div>
          </div>

          {/* DYNAMIC FILTER & SORTING TOOLBAR */}
          <div className="bg-white border border-gray-200 rounded-lg shadow-sm mb-6 p-4 flex justify-between items-center">
            <div className="flex items-center gap-2">
              <Filter size={18} className="text-gray-500" />
              <span className="font-bold text-sm text-gray-700 mr-2">시리즈 필터:</span>
              <div className="flex gap-2 flex-wrap">
                {seriesOptions.map(series => (
                  <button 
                    key={series}
                    onClick={() => setSelectedSeries(series)}
                    className={`px-3 py-1.5 text-xs font-bold rounded-full transition-colors border ${selectedSeries === series ? 'bg-[#00b050] text-white border-[#00b050]' : 'bg-white text-gray-600 border-gray-300 hover:bg-gray-50'}`}
                  >
                    {series}
                  </button>
                ))}
              </div>
            </div>
            
            <div className="flex items-center">
               <select 
                 className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#00b050] focus:border-[#00b050] block p-2 outline-none font-medium"
                 value={sortBy}
                 onChange={(e) => setSortBy(e.target.value as any)}
               >
                 <option value="PRICE_ASC">낮은 가격순</option>
                 <option value="VRAM_DESC">VRAM 높은순</option>
               </select>
            </div>
          </div>

          {error && <div className="bg-red-50 text-red-600 p-4 rounded-lg border border-red-200 mb-6 text-sm font-bold">오류: {error}</div>}

          {/* PRODUCT LISTING */}
          <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
            <div className="border-b border-gray-200 px-6 py-4 flex justify-between items-center bg-gray-50/50 rounded-t-lg">
              <h3 className="font-bold text-gray-900 text-lg flex items-center">
                <span className="bg-red-500 text-white text-xs px-2 py-0.5 rounded-sm mr-2 animate-pulse">LIVE</span>
                클라우드 GPU 실시간 최저가 비교
              </h3>
              <div className="text-sm text-gray-500 font-medium">총 <span className="text-[#00b050] font-bold">{filteredAndSortedGpus.length}</span>개의 상품</div>
            </div>

            <div className="divide-y divide-gray-100">
              {filteredAndSortedGpus.map((gpu) => {
                const sortedOffers = [...gpu.offers].sort((a, b) => a.price_per_hour - b.price_per_hour);
                const lowestOffer = sortedOffers[0];
                const isPremium = gpu.name.includes("A100") || gpu.name.includes("H100") || gpu.name.includes("4090");
                const isChartOpen = selectedChartGpu === gpu.id;

                return (
                  <div key={gpu.id} className="p-6 flex flex-col hover:bg-gray-50/50 transition-colors">
                    <div className="flex gap-6 w-full">
                      {/* Thumbnail */}
                      <div className="w-[160px] h-[160px] bg-white border border-gray-200 flex-shrink-0 rounded-md flex items-center justify-center relative shadow-sm p-4">
                        {isPremium && <div className="absolute -top-2 -left-2 bg-red-500 text-white text-[10px] font-bold px-2 py-1 rounded shadow-md transform -rotate-6">인기폭발</div>}
                        <div className="text-center w-full">
                          <ImageIcon size={48} className="mx-auto text-gray-300 mb-2" strokeWidth={1} />
                          <div className="text-xs font-bold text-gray-400 truncate w-full">{gpu.name}</div>
                        </div>
                      </div>

                      {/* Product Details */}
                      <div className="flex-1 flex flex-col justify-between">
                        <div>
                          <div className="flex items-center mb-1">
                            <span className="text-xs font-bold text-[#00b050] bg-green-50 px-2 py-0.5 rounded mr-2 border border-green-100">무료배송(즉시할당)</span>
                          </div>
                          <h4 className="text-xl font-bold text-gray-900 hover:text-blue-600 hover:underline cursor-pointer leading-tight mb-2">
                            {gpu.name} <span className="text-gray-500 font-medium text-lg"> ({gpu.vram_gb}GB VRAM)</span>
                          </h4>
                          
                          <div className="text-sm text-gray-600 leading-relaxed mb-4 line-clamp-2">
                            초고성능 연산용 GPU / VRAM: {gpu.vram_gb}GB / {lowestOffer?.sys_ram_gb ? `권장 시스템 RAM: ${lowestOffer.sys_ram_gb}GB / ` : ''} {lowestOffer?.tdp_w ? `소비전력: ${lowestOffer.tdp_w}W / ` : ''} AI 딥러닝 최적화 / CUDA 지원
                          </div>
                        </div>

                        {/* Best Price Summary */}
                        <div className="flex items-end justify-between border-t border-dashed border-gray-200 pt-4">
                          <div className="flex items-center gap-2">
                            <span className="text-sm font-bold text-gray-500">최저가</span>
                            {lowestOffer ? (
                              <>
                                <span className="text-2xl font-black text-red-600 tracking-tighter">
                                  ${lowestOffer.price_per_hour.toFixed(3)}
                                </span>
                                <span className="text-sm text-gray-500">/시간</span>
                              </>
                            ) : (
                              <span className="text-gray-400 font-medium">재고없음</span>
                            )}
                          </div>
                          
                          <div className="flex gap-2">
                            <button 
                              onClick={() => setSelectedChartGpu(isChartOpen ? null : gpu.id)}
                              className={`border text-sm font-bold px-4 py-2 rounded shadow-sm transition-colors flex items-center ${isChartOpen ? 'bg-gray-800 text-white border-gray-800' : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'}`}
                            >
                              <TrendingUp size={16} className="mr-1.5" /> 
                              {isChartOpen ? '차트 닫기' : '시세 차트'}
                            </button>
                            {lowestOffer && (
                              <a 
                                href={lowestOffer.provider_link || "#"}
                                target="_blank"
                                rel="noopener noreferrer" 
                                className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold px-6 py-2 rounded shadow-sm transition-colors flex items-center"
                              >
                                최저가 보러가기 <ChevronRight size={16} className="ml-1" />
                              </a>
                            )}
                          </div>
                        </div>
                      </div>

                      {/* Providers List Column */}
                      <div className="w-[280px] flex-shrink-0 border-l border-gray-100 pl-6 hidden lg:block">
                        <div className="text-sm font-bold text-gray-900 mb-3 flex items-center justify-between">
                          판매처 비교 <span className="bg-gray-100 text-gray-500 text-[10px] px-1.5 rounded">{sortedOffers.length}몰</span>
                        </div>
                        <div className="space-y-3">
                          {sortedOffers.slice(0, 4).map((offer, idx) => (
                            <a 
                              key={idx} 
                              href={offer.provider_link || "#"}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="flex justify-between items-center group cursor-pointer"
                            >
                              <span className="text-sm text-gray-600 group-hover:text-blue-600 group-hover:underline truncate w-1/2 capitalize font-medium flex items-center">
                                {offer.provider}
                                {idx === 0 && <span className="ml-1 text-[10px] bg-red-50 text-red-500 border border-red-200 px-1 rounded">최저</span>}
                              </span>
                              <span className="text-sm font-bold text-gray-900 group-hover:text-blue-600">
                                ${offer.price_per_hour.toFixed(3)}
                              </span>
                            </a>
                          ))}
                        </div>
                      </div>
                    </div>

                    {/* Chart Dropdown Section */}
                    {isChartOpen && lowestOffer && (
                      <div className="mt-4 pt-4 border-t border-gray-100 animate-in fade-in slide-in-from-top-4 duration-300">
                        <GpuCandlestickChart gpuName={gpu.name} basePrice={lowestOffer.price_per_hour} />
                      </div>
                    )}

                  </div>
                );
              })}
              
              {filteredAndSortedGpus.length === 0 && !loading && (
                <div className="py-20 text-center text-gray-500 flex flex-col items-center">
                  <Search size={48} className="text-gray-300 mb-4" strokeWidth={1} />
                  <p className="font-bold text-lg text-gray-700 mb-1">조건에 맞는 상품이 없습니다.</p>
                  <p className="text-sm">필터를 변경하거나 다른 모델명으로 검색해보세요.</p>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
