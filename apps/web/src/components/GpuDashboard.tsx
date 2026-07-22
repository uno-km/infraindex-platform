"use client";

import { useEffect, useState } from "react";
import { Zap, Search, Menu, User, Clock, Heart, ChevronRight, ChevronLeft, Image as ImageIcon } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer, Cell } from "recharts";

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

// Chart specific component to avoid hydration mismatches
const PriceComparisonChart = ({ data }: { data: any[] }) => {
  return (
    <div className="bg-white p-6 rounded-lg border border-gray-200 mb-6 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-gray-900 text-lg">💡 주요 GPU 시간당 평균 요금 (온디맨드 기준)</h3>
        <span className="text-xs text-gray-500">단위: USD/hr</span>
      </div>
      <div className="h-[250px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
            <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6B7280' }} dy={10} />
            <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#6B7280' }} />
            <RechartsTooltip 
              cursor={{ fill: '#F3F4F6' }} 
              contentStyle={{ borderRadius: '8px', border: '1px solid #E5E7EB', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
              formatter={(value: number) => [`$${value.toFixed(2)}`, '평균 가격']}
            />
            <Bar dataKey="avgPrice" radius={[4, 4, 0, 0]} maxBarSize={50}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.name.includes('A100') || entry.name.includes('H100') ? '#00b050' : '#3B82F6'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default function GpuDashboard() {
  const [gpus, setGpus] = useState<GpuModel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

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

  // Filter GPUs based on search
  const filteredGpus = gpus.filter(g => g.name.toLowerCase().includes(searchQuery.toLowerCase()));

  // Prepare chart data (Top 5 popular GPUs average price)
  const chartData = gpus
    .map(g => {
      const validOffers = g.offers.filter(o => o.price_per_hour > 0);
      const avgPrice = validOffers.length > 0 
        ? validOffers.reduce((sum, o) => sum + o.price_per_hour, 0) / validOffers.length 
        : 0;
      return { name: g.name, avgPrice };
    })
    .filter(d => d.avgPrice > 0)
    .sort((a, b) => b.avgPrice - a.avgPrice)
    .slice(0, 8); // Show top 8 expensive/popular GPUs

  // Mock categories for the sidebar
  const categories = [
    { icon: "💻", name: "컴퓨터·노트북·조립PC", active: true },
    { icon: "📱", name: "태블릿·모바일·디카" },
    { icon: "📺", name: "가전·TV" },
    { icon: "⚽", name: "스포츠·골프" },
    { icon: "🚗", name: "자동차·용품·공구" },
    { icon: "🛋️", name: "가구·조명" },
    { icon: "🍎", name: "식품·유아·완구" },
    { icon: "🧼", name: "생활·주방·건강" },
    { icon: "👗", name: "패션·잡화·뷰티" },
  ];

  if (loading) return <div className="h-screen flex items-center justify-center"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#00b050]"></div></div>;

  return (
    <div className="min-h-screen bg-[#F8F9FA] font-sans text-gray-900 pb-20">
      {/* HEADER */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
        {/* Top Utility Bar */}
        <div className="bg-gray-100 text-xs text-gray-500 py-1">
          <div className="max-w-[1200px] mx-auto flex justify-end gap-4 px-4">
            <span className="hover:text-gray-900 cursor-pointer">에누리</span>
            <span className="hover:text-gray-900 cursor-pointer">몰테일</span>
            <span className="hover:text-gray-900 cursor-pointer">플레이오토</span>
          </div>
        </div>
        
        {/* Main Header Area */}
        <div className="max-w-[1200px] mx-auto flex items-center justify-between py-6 px-4">
          <div className="flex items-center gap-10">
            {/* Logo */}
            <div className="text-3xl font-black text-[#00b050] tracking-tighter cursor-pointer flex items-end">
              GPUawa <span className="text-xs text-gray-500 font-normal ml-2 mb-1 tracking-normal">비교하고 잘 사는 GPU와</span>
            </div>
          </div>

          {/* Search Bar */}
          <div className="flex-1 max-w-[500px] mx-10">
            <div className="relative flex items-center">
              <input 
                type="text" 
                placeholder="A100, H100 등 GPU 모델명을 검색해보세요" 
                className="w-full border-2 border-[#00b050] rounded-full py-3 px-6 pr-14 text-sm font-medium outline-none focus:ring-2 focus:ring-[#00b050]/20"
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
              />
              <button className="absolute right-4 text-[#00b050]">
                <Search size={24} strokeWidth={2.5} />
              </button>
            </div>
            <div className="flex gap-3 mt-2 justify-center text-xs text-[#00b050] font-medium">
              <span className="bg-blue-50 text-blue-600 px-2 py-0.5 rounded text-[10px] font-bold">최대 52만원 지원</span>
              <span className="hover:underline cursor-pointer">인터넷 가입</span>
              <span className="hover:underline cursor-pointer">이벤트/체험단</span>
            </div>
          </div>

          {/* User Icons */}
          <div className="flex gap-6 items-center">
            <div className="flex flex-col items-center cursor-pointer hover:text-[#00b050] transition-colors">
              <Clock size={28} strokeWidth={1.5} className="text-gray-600 mb-1" />
              <span className="text-xs">최근</span>
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
                실시간 인기 GPU 대여 견적 확실하게 줄이는 법
              </div>
              <h2 className="text-2xl font-bold">A100 · H100 렌탈료 최대 37%↓</h2>
            </div>
            <div className="absolute right-0 top-0 h-full w-1/2 bg-gradient-to-l from-black/80 to-transparent z-0"></div>
            {/* Generic GPU Image placeholder */}
            <div className="z-10 bg-gray-800/80 p-4 rounded-xl border border-gray-700 shadow-2xl transform rotate-3">
               <div className="flex gap-1 mb-1"><div className="w-2 h-2 rounded-full bg-red-500"></div><div className="w-2 h-2 rounded-full bg-yellow-500"></div><div className="w-2 h-2 rounded-full bg-green-500"></div></div>
               <div className="text-[#00ff88] font-mono text-sm border-b border-gray-600 pb-1 mb-1">NVIDIA H100 SXM</div>
               <div className="text-xs text-gray-300 font-mono">VRAM: 80GB<br/>TDP: 700W</div>
            </div>
          </div>

          {/* CHART AREA */}
          {chartData.length > 0 && <PriceComparisonChart data={chartData} />}

          {/* ERROR ALERT */}
          {error && (
            <div className="bg-red-50 text-red-600 p-4 rounded-lg border border-red-200 mb-6 text-sm font-bold">
              오류: {error}
            </div>
          )}

          {/* PRODUCT LISTING (Danawa Style) */}
          <div className="bg-white border border-gray-200 rounded-lg shadow-sm">
            <div className="border-b border-gray-200 px-6 py-4 flex justify-between items-center bg-gray-50/50 rounded-t-lg">
              <h3 className="font-bold text-gray-900 text-lg flex items-center">
                <span className="bg-red-500 text-white text-xs px-2 py-0.5 rounded-sm mr-2 animate-pulse">LIVE</span>
                클라우드 GPU 실시간 최저가 비교
              </h3>
              <div className="text-sm text-gray-500 font-medium">총 <span className="text-[#00b050] font-bold">{filteredGpus.length}</span>개의 상품</div>
            </div>

            <div className="divide-y divide-gray-100">
              {filteredGpus.map((gpu) => {
                // Sort offers by price ascending
                const sortedOffers = [...gpu.offers].sort((a, b) => a.price_per_hour - b.price_per_hour);
                const lowestOffer = sortedOffers[0];
                const isPremium = gpu.name.includes("A100") || gpu.name.includes("H100") || gpu.name.includes("4090");

                return (
                  <div key={gpu.id} className="p-6 flex gap-6 hover:bg-gray-50/50 transition-colors">
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
                          <span className="text-xs font-bold text-[#00b050] bg-green-50 px-2 py-0.5 rounded mr-2 border border-green-100">무료배송(클라우드 즉시할당)</span>
                          <span className="text-xs text-gray-400">등록월: 2024.01</span>
                        </div>
                        <h4 className="text-xl font-bold text-gray-900 hover:text-blue-600 hover:underline cursor-pointer leading-tight mb-2">
                          {gpu.name} <span className="text-gray-500 font-medium text-lg"> ({gpu.vram_gb}GB VRAM)</span>
                        </h4>
                        
                        <div className="text-sm text-gray-600 leading-relaxed mb-4 line-clamp-2">
                          초고성능 연산용 GPU / VRAM: {gpu.vram_gb}GB / {lowestOffer?.sys_ram_gb ? `권장 시스템 RAM: ${lowestOffer.sys_ram_gb}GB / ` : ''} {lowestOffer?.tdp_w ? `소비전력: ${lowestOffer.tdp_w}W / ` : ''} 클라우드 인스턴스 전용 / AI 딥러닝 최적화 / CUDA 지원
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
                           <button className="bg-white border border-gray-300 text-gray-700 text-sm font-bold px-4 py-2 rounded shadow-sm hover:bg-gray-50">찜하기</button>
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
                      {sortedOffers.length > 4 && (
                        <div className="text-center mt-3 pt-3 border-t border-gray-50">
                          <button className="text-xs text-gray-500 hover:text-gray-900 flex items-center justify-center w-full">
                            더보기 <ChevronRight size={12} />
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
              
              {filteredGpus.length === 0 && !loading && (
                <div className="py-20 text-center text-gray-500 flex flex-col items-center">
                  <Search size={48} className="text-gray-300 mb-4" strokeWidth={1} />
                  <p className="font-bold text-lg text-gray-700 mb-1">검색 결과가 없습니다.</p>
                  <p className="text-sm">다른 모델명으로 검색해보세요.</p>
                </div>
              )}
            </div>
          </div>

        </main>
      </div>
    </div>
  );
}
