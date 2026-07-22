"use client";

import { useEffect, useState, useMemo } from "react";
import { Search, Menu, User, Activity, Bookmark, ChevronRight, Server, Cpu, HardDrive, Cloud, Info, ExternalLink, List } from "lucide-react";
import dynamic from "next/dynamic";

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

const GpuCandlestickChart = ({ gpuName, basePrice, exchangeRate, providers, period }: { gpuName: string, basePrice: number, exchangeRate: number, providers: string[], period: "DAY" | "WEEK" | "MONTH" }) => {
  const chartData = useMemo(() => {
    const rawData = [];
    let currentPrice = basePrice;
    const now = new Date();
    
    // Generate 90 days of base data
    for (let i = 90; i >= 0; i--) {
      const date = new Date(now.getTime() - i * 24 * 60 * 60 * 1000);
      const volatility = currentPrice * 0.05; 
      const open = currentPrice + (Math.random() - 0.5) * volatility;
      const close = open + (Math.random() - 0.5) * volatility;
      const high = Math.max(open, close) + Math.random() * volatility;
      const low = Math.min(open, close) - Math.random() * volatility;
      
      rawData.push({ date, open, high, low, close });
      currentPrice = close;
    }

    // Aggregate based on period
    const aggregated = [];
    let chunkSize = period === "DAY" ? 1 : period === "WEEK" ? 7 : 30;
    
    for (let i = 0; i < rawData.length; i += chunkSize) {
      const chunk = rawData.slice(i, i + chunkSize);
      const date = chunk[chunk.length - 1].date;
      const open = chunk[0].open;
      const close = chunk[chunk.length - 1].close;
      const high = Math.max(...chunk.map(d => d.high));
      const low = Math.min(...chunk.map(d => d.low));
      
      aggregated.push({
        x: date,
        y: [
          parseFloat((open * exchangeRate).toFixed(exchangeRate === 1 ? 3 : 0)),
          parseFloat((high * exchangeRate).toFixed(exchangeRate === 1 ? 3 : 0)),
          parseFloat((low * exchangeRate).toFixed(exchangeRate === 1 ? 3 : 0)),
          parseFloat((close * exchangeRate).toFixed(exchangeRate === 1 ? 3 : 0))
        ],
        highProvider: providers[Math.floor(Math.random() * providers.length)] || "Unknown",
        lowProvider: providers[Math.floor(Math.random() * providers.length)] || "Unknown"
      });
    }

    // Slice to show only relevant timeframe (30 days, ~12 weeks, ~6 months)
    const displayCount = period === "DAY" ? 30 : period === "WEEK" ? 12 : 6;
    const finalData = aggregated.slice(-displayCount);

    // Calculate 5-period Simple Moving Average (SMA) for trendline
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
  }, [basePrice, exchangeRate, period]);

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
    colors: ['#000000', '#8b5cf6'], // Line color is purple
    title: { text: `${gpuName} 가격 변동 추이`, align: 'left', style: { fontSize: '15px', fontWeight: '700', color: '#1e293b' } },
    xaxis: { type: 'datetime', labels: { style: { colors: '#64748b', fontSize: '12px', fontWeight: 500 } }, axisBorder: { show: false }, axisTicks: { show: false } },
    yaxis: { 
      tooltip: { enabled: true }, 
      labels: { style: { colors: '#64748b', fontWeight: 500 }, formatter: (val: number) => `${currencySymbol}${val ? val.toLocaleString() : ''}` } 
    },
    tooltip: {
      shared: true,
      custom: function({seriesIndex, dataPointIndex, w}: any) {
        if (seriesIndex !== 0) return ''; // Only show custom tooltip for candlestick
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
            <div class="mt-1 flex justify-between gap-4 pt-1 border-t border-slate-100"><span>종가 (Close):</span> <strong>${currencySymbol}${c}</strong></div>
            ${lineData.y ? `<div class="mt-1 flex justify-between gap-4 text-purple-600"><span>추세선 (SMA 5):</span> <strong>${currencySymbol}${lineData.y}</strong></div>` : ''}
          </div>
        `;
      }
    },
    plotOptions: {
      candlestick: {
        colors: { upward: '#ef4444', downward: '#3b82f6' }, // 한국 주식 스타일 (상승 빨강, 하락 파랑)
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
};

export default function GpuDashboard() {
  const [gpus, setGpus] = useState<GpuModel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  
  const [selectedSeries, setSelectedSeries] = useState<string>("전체보기");
  const [sortBy, setSortBy] = useState<"PRICE_ASC" | "VRAM_DESC">("PRICE_ASC");
  
  const [selectedChartGpu, setSelectedChartGpu] = useState<string | null>(null);
  const [chartPeriod, setChartPeriod] = useState<"DAY" | "WEEK" | "MONTH">("DAY");

  const [expandedProvidersGpu, setExpandedProvidersGpu] = useState<string | null>(null);

  // Currency State
  const [currency, setCurrency] = useState<"USD" | "KRW">("USD");
  const [krwRate, setKrwRate] = useState<number>(1);

  useEffect(() => {
    async function fetchExchangeRate() {
      try {
        const res = await fetch("https://open.er-api.com/v6/latest/USD");
        const data = await res.json();
        if (data && data.rates && data.rates.KRW) {
          setKrwRate(data.rates.KRW);
        }
      } catch (err) {
        console.error("Failed to fetch exchange rate", err);
      }
    }
    fetchExchangeRate();

    async function fetchGpus() {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        const res = await fetch(`${apiUrl}/api/v1/gpus`);
        if (!res.ok) throw new Error("데이터를 불러오는데 실패했습니다.");
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

  const exchangeMultiplier = currency === "KRW" ? krwRate : 1;
  const formatPrice = (price: number) => {
    const val = price * exchangeMultiplier;
    return currency === "KRW" 
      ? `₩${val.toLocaleString(undefined, { maximumFractionDigits: 0 })}` 
      : `$${val.toFixed(3)}`;
  };

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
    return ["전체보기", ...Array.from(seriesSet)];
  }, [gpus]);

  const filteredAndSortedGpus = useMemo(() => {
    let result = gpus.filter(g => g.name.toLowerCase().includes(searchQuery.toLowerCase()));
    
    if (selectedSeries !== "전체보기") {
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

  const categories = [
    { icon: <Server size={18}/>, name: "GPU 인스턴스", active: true },
    { icon: <Cpu size={18}/>, name: "CPU 컴퓨팅" },
    { icon: <HardDrive size={18}/>, name: "스토리지 & 블록" },
    { icon: <Cloud size={18}/>, name: "베어메탈 서버" },
  ];

  if (loading) return <div className="h-screen flex items-center justify-center bg-slate-50"><div className="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600"></div></div>;

  return (
    <div className="min-h-screen bg-slate-50/50 font-sans text-slate-900 pb-24 selection:bg-indigo-100">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-slate-200/80 sticky top-0 z-50 shadow-[0_4px_30px_rgb(0,0,0,0.03)]">
        <div className="max-w-7xl mx-auto flex items-center justify-between py-4 px-6">
          <div className="flex items-center gap-8">
            <div className="text-2xl font-black text-indigo-600 tracking-tight cursor-pointer flex items-center">
              <Cloud className="mr-2" size={28} strokeWidth={2.5} /> InfraIndex
              <span className="text-xs text-slate-400 font-medium ml-4 tracking-normal hidden md:inline-block border-l border-slate-200 pl-4 py-1">글로벌 클라우드 자원 거래소</span>
            </div>
          </div>

          <div className="flex-1 max-w-lg mx-8">
            <div className="relative flex items-center group">
              <input 
                type="text" 
                placeholder="검색할 자원 모델명 입력 (예: H100, RTX 4090)" 
                className="w-full bg-slate-100/50 border border-slate-200 focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-50 rounded-2xl py-2.5 px-5 text-sm outline-none transition-all duration-300"
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
              />
              <button className="absolute right-4 text-slate-400 group-focus-within:text-indigo-600 transition-colors">
                <Search size={18} />
              </button>
            </div>
          </div>

          <div className="flex gap-7 items-center text-slate-500">
            <div className="flex items-center gap-2 cursor-pointer hover:text-indigo-600 transition-colors">
              <Activity size={18} />
              <span className="text-sm font-semibold hidden sm:block">시장 데이터</span>
            </div>
            <div className="flex items-center gap-2 cursor-pointer hover:text-indigo-600 transition-colors">
              <Bookmark size={18} />
              <span className="text-sm font-semibold hidden sm:block">관심 자원</span>
            </div>
            <div className="flex items-center gap-2 cursor-pointer bg-slate-900 hover:bg-indigo-600 text-white px-4 py-2 rounded-xl transition-all shadow-md shadow-slate-200 hover:shadow-indigo-200">
              <User size={16} />
              <span className="text-sm font-semibold hidden sm:block">로그인</span>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto mt-8 px-6 flex gap-8 items-start">
        
        {/* Sidebar */}
        <aside className="w-64 flex-shrink-0 bg-white border border-slate-200/60 rounded-3xl overflow-hidden sticky top-[100px] shadow-[0_8px_30px_rgb(0,0,0,0.04)]">
          <div className="bg-white text-slate-800 py-5 px-6 flex items-center font-extrabold text-sm tracking-wide border-b border-slate-100">
            <Menu className="mr-3 text-slate-400" size={18} /> 리소스 카테고리
          </div>
          <ul className="py-2">
            {categories.map((cat, idx) => (
              <li key={idx} className={`px-6 py-3.5 text-sm font-semibold border-b border-slate-50 last:border-0 cursor-pointer flex justify-between items-center transition-all duration-200 ${cat.active ? 'bg-indigo-50/50 text-indigo-700 border-l-4 border-indigo-600 pl-5' : 'text-slate-500 hover:bg-slate-50 hover:text-indigo-600'}`}>
                <span className="flex items-center gap-3">
                  <span className={`${cat.active ? 'text-indigo-500' : 'text-slate-400'}`}>{cat.icon}</span>
                  {cat.name}
                </span>
                {cat.active && <ChevronRight size={16} className="text-indigo-400" />}
              </li>
            ))}
          </ul>
        </aside>

        {/* Main Content */}
        <main className="flex-1 min-w-0">
          
          <div className="bg-white/80 backdrop-blur-sm border border-slate-200/60 rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] mb-8 p-5 px-6 flex justify-between items-center flex-wrap gap-4">
            <div className="flex items-center gap-4">
              <span className="font-extrabold text-sm text-slate-800 bg-slate-100 px-3 py-1 rounded-lg">필터링</span>
              <div className="flex gap-2 flex-wrap">
                {seriesOptions.map(series => (
                  <button 
                    key={series}
                    onClick={() => setSelectedSeries(series)}
                    className={`px-4 py-2 text-xs font-bold rounded-xl transition-all duration-200 border ${selectedSeries === series ? 'bg-slate-900 text-white border-slate-900 shadow-md shadow-slate-200' : 'bg-white text-slate-500 border-slate-200 hover:bg-slate-50 hover:border-slate-300'}`}
                  >
                    {series}
                  </button>
                ))}
              </div>
            </div>
            
            <div className="flex items-center gap-4">
               <div className="flex bg-slate-100/80 p-1.5 rounded-xl border border-slate-200/50">
                 <button 
                   onClick={() => setCurrency("USD")}
                   className={`px-4 py-1.5 text-xs font-bold rounded-lg transition-all duration-200 ${currency === "USD" ? 'bg-white shadow-sm text-slate-900' : 'text-slate-500 hover:text-slate-800'}`}
                 >
                   $ USD (달러)
                 </button>
                 <button 
                   onClick={() => setCurrency("KRW")}
                   className={`px-4 py-1.5 text-xs font-bold rounded-lg transition-all duration-200 ${currency === "KRW" ? 'bg-white shadow-sm text-slate-900' : 'text-slate-500 hover:text-slate-800'}`}
                 >
                   ₩ KRW (원화)
                 </button>
               </div>
               <select 
                 className="bg-white border border-slate-200 text-slate-700 text-sm rounded-xl focus:ring-4 focus:ring-indigo-50 focus:border-indigo-500 outline-none px-4 py-2 font-semibold shadow-sm transition-all cursor-pointer"
                 value={sortBy}
                 onChange={(e) => setSortBy(e.target.value as any)}
               >
                 <option value="PRICE_ASC">최저가 순 정렬</option>
                 <option value="VRAM_DESC">VRAM 높은 순 정렬</option>
               </select>
            </div>
          </div>

          {error && <div className="bg-rose-50 text-rose-600 p-5 rounded-2xl border border-rose-200 mb-6 text-sm font-semibold flex items-center shadow-sm"><Activity className="mr-2" size={18}/> {error}</div>}

          <div className="bg-white border border-slate-200/60 rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] overflow-hidden">
            <div className="border-b border-slate-100 px-8 py-5 flex justify-between items-center bg-white">
              <h3 className="font-extrabold text-slate-900 flex items-center text-lg">
                <span className="relative flex h-3 w-3 mr-3">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
                </span>
                글로벌 GPU 인스턴스 시세표
              </h3>
              <div className="text-sm text-slate-500 font-medium bg-slate-50 px-3 py-1 rounded-lg border border-slate-100">총 검색 결과: <span className="text-indigo-600 font-bold">{filteredAndSortedGpus.length}</span> 건</div>
            </div>

            <div className="divide-y divide-slate-100/80">
              {filteredAndSortedGpus.map((gpu) => {
                const sortedOffers = [...gpu.offers].sort((a, b) => a.price_per_hour - b.price_per_hour);
                const lowestOffer = sortedOffers[0];
                const highestOffer = sortedOffers[sortedOffers.length - 1];
                const avgPrice = sortedOffers.reduce((acc, curr) => acc + curr.price_per_hour, 0) / sortedOffers.length;
                
                const isChartOpen = selectedChartGpu === gpu.id;
                const isProvidersExpanded = expandedProvidersGpu === gpu.id;

                return (
                  <div key={gpu.id} className="p-8 flex flex-col hover:bg-slate-50/40 transition-colors duration-300 group">
                    <div className="flex gap-8 w-full items-start">
                      
                      {/* Product Overview */}
                      <div className="flex-1">
                        <div className="flex items-center mb-3 gap-2">
                          <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-md tracking-wider border border-emerald-100/50">즉시 할당 가능</span>
                        </div>
                        <h4 className="text-2xl font-black text-slate-900 leading-tight mb-2 tracking-tight">
                          {gpu.name} <span className="text-slate-400 font-semibold text-lg ml-1 font-mono">({gpu.vram_gb}GB VRAM)</span>
                        </h4>
                        
                        <div className="text-sm text-slate-500 leading-relaxed mb-6 flex flex-wrap gap-x-5 gap-y-2 font-medium">
                          <span className="flex items-center"><Activity size={14} className="mr-1.5 text-slate-400"/> AI 딥러닝 & 추론 최적화</span>
                          {lowestOffer?.sys_ram_gb ? <span className="flex items-center"><HardDrive size={14} className="mr-1.5 text-slate-400"/> 시스템 RAM: {lowestOffer.sys_ram_gb}GB</span> : null}
                          {lowestOffer?.tdp_w ? <span className="flex items-center"><Cpu size={14} className="mr-1.5 text-slate-400"/> TDP: {lowestOffer.tdp_w}W</span> : null}
                        </div>

                        <div className="flex items-center gap-3">
                          <button 
                            onClick={() => setSelectedChartGpu(isChartOpen ? null : gpu.id)}
                            className={`border text-sm font-bold px-5 py-2.5 rounded-xl transition-all duration-200 flex items-center ${isChartOpen ? 'bg-indigo-600 text-white border-indigo-600 shadow-md shadow-indigo-200' : 'bg-white border-slate-200 text-slate-700 hover:border-slate-300 hover:bg-slate-50 shadow-sm'}`}
                          >
                            <Activity size={16} className={`mr-2 ${isChartOpen ? 'text-indigo-200' : 'text-indigo-500'}`} /> 
                            {isChartOpen ? '차트 닫기' : '시세 차트 분석'}
                          </button>
                          
                          <button 
                            onClick={() => setExpandedProvidersGpu(isProvidersExpanded ? null : gpu.id)}
                            className={`border text-sm font-bold px-5 py-2.5 rounded-xl transition-all duration-200 flex items-center ${isProvidersExpanded ? 'bg-slate-800 text-white border-slate-800 shadow-md' : 'bg-white border-slate-200 text-slate-700 hover:border-slate-300 hover:bg-slate-50 shadow-sm'}`}
                          >
                            <List size={16} className={`mr-2 ${isProvidersExpanded ? 'text-slate-300' : 'text-slate-500'}`} /> 
                            판매처 전체보기 ({sortedOffers.length}곳)
                          </button>
                        </div>
                      </div>

                      {/* Pricing Intel Column */}
                      <div className="w-[280px] bg-slate-50 rounded-2xl p-5 border border-slate-100 group-hover:border-slate-200 transition-all shadow-[inset_0_2px_10px_rgba(0,0,0,0.01)] relative">
                        <div className="text-xs font-black text-slate-400 tracking-widest mb-4 flex items-center">
                          <div className="h-1 w-1 rounded-full bg-slate-300 mr-2"></div>
                          실시간 가격 동향
                        </div>
                        
                        <div className="space-y-4">
                          <div className="flex justify-between items-center group/tooltip relative">
                            <span className="text-sm font-semibold text-slate-500 flex items-center">최저가 <Info size={14} className="ml-1.5 text-slate-300 cursor-help"/></span>
                            <span className="text-xl font-black text-emerald-600 tracking-tight">{formatPrice(lowestOffer?.price_per_hour || 0)}</span>
                            {/* Tooltip */}
                            <div className="absolute bottom-full right-0 mb-2 hidden group-hover/tooltip:block bg-slate-900 text-white text-xs px-3 py-2 rounded-lg shadow-xl whitespace-nowrap z-10 font-medium">
                              제공사: <span className="font-bold capitalize text-emerald-300">{lowestOffer?.provider}</span>
                            </div>
                          </div>

                          <div className="flex justify-between items-center group/tooltip relative border-y border-slate-200/60 py-3">
                            <span className="text-sm font-semibold text-slate-500 flex items-center">평균가 <Info size={14} className="ml-1.5 text-slate-300 cursor-help"/></span>
                            <span className="text-base font-bold text-slate-700">{formatPrice(avgPrice)}</span>
                            <div className="absolute bottom-full right-0 mb-2 hidden group-hover/tooltip:block bg-slate-900 text-white text-xs px-3 py-2 rounded-lg shadow-xl whitespace-nowrap z-10 font-medium">
                              전 세계 {sortedOffers.length}개 업체의 평균 단가
                            </div>
                          </div>

                          <div className="flex justify-between items-center group/tooltip relative">
                            <span className="text-sm font-semibold text-slate-500 flex items-center">최고가 <Info size={14} className="ml-1.5 text-slate-300 cursor-help"/></span>
                            <span className="text-base font-bold text-rose-500">{formatPrice(highestOffer?.price_per_hour || 0)}</span>
                            <div className="absolute bottom-full right-0 mb-2 hidden group-hover/tooltip:block bg-slate-900 text-white text-xs px-3 py-2 rounded-lg shadow-xl whitespace-nowrap z-10 font-medium">
                              제공사: <span className="font-bold capitalize text-rose-300">{highestOffer?.provider}</span>
                            </div>
                          </div>
                        </div>

                        {lowestOffer && (
                          <a 
                            href={lowestOffer.provider_link || "#"}
                            target="_blank"
                            rel="noopener noreferrer" 
                            className="mt-5 w-full bg-slate-900 hover:bg-indigo-600 text-white text-sm font-bold py-3 rounded-xl shadow-md transition-all flex items-center justify-center group/btn"
                          >
                            최저가로 바로 할당하기 <ChevronRight size={16} className="ml-1 opacity-60 group-hover/btn:translate-x-1 transition-transform" />
                          </a>
                        )}
                      </div>

                    </div>

                    {/* Providers Expanded List */}
                    {isProvidersExpanded && (
                      <div className="mt-6 pt-6 border-t border-slate-100 animate-in slide-in-from-top-4 fade-in duration-300">
                        <h5 className="font-bold text-slate-800 mb-4 flex items-center"><List size={16} className="mr-2 text-indigo-500"/> 전체 판매처 목록</h5>
                        <div className="bg-slate-50 rounded-xl border border-slate-200 overflow-hidden">
                          <table className="w-full text-left text-sm">
                            <thead className="bg-slate-100/50 text-slate-500 font-semibold border-b border-slate-200">
                              <tr>
                                <th className="py-3 px-4">제공사 (Provider)</th>
                                <th className="py-3 px-4">리전 (Region)</th>
                                <th className="py-3 px-4">시간당 단가</th>
                                <th className="py-3 px-4 text-right">바로가기</th>
                              </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-100 text-slate-700">
                              {sortedOffers.map((offer, idx) => (
                                <tr key={idx} className="hover:bg-white transition-colors">
                                  <td className="py-3 px-4 font-bold capitalize flex items-center">
                                    {offer.provider}
                                    {idx === 0 && <span className="ml-2 text-[10px] bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded border border-emerald-200">최저가</span>}
                                  </td>
                                  <td className="py-3 px-4 text-slate-500">{offer.region}</td>
                                  <td className="py-3 px-4 font-mono font-medium">{formatPrice(offer.price_per_hour)}</td>
                                  <td className="py-3 px-4 text-right">
                                    <a href={offer.provider_link || "#"} target="_blank" rel="noopener noreferrer" className="text-indigo-600 hover:text-indigo-800 font-semibold flex items-center justify-end">
                                      링크 이동 <ExternalLink size={14} className="ml-1"/>
                                    </a>
                                  </td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    )}

                    {/* Candlestick Chart */}
                    {isChartOpen && lowestOffer && (
                      <div className="mt-6 pt-6 border-t border-slate-100 animate-in slide-in-from-top-4 fade-in duration-300">
                        <div className="flex justify-between items-center mb-2">
                          <div className="text-sm font-bold text-slate-700">고급 차트 분석 (이동평균선 포함)</div>
                          <div className="flex bg-slate-100 p-1 rounded-lg border border-slate-200/50">
                            <button onClick={() => setChartPeriod("DAY")} className={`px-4 py-1 text-xs font-bold rounded-md transition-all ${chartPeriod === "DAY" ? 'bg-white shadow-sm text-indigo-600' : 'text-slate-500 hover:text-slate-800'}`}>일봉</button>
                            <button onClick={() => setChartPeriod("WEEK")} className={`px-4 py-1 text-xs font-bold rounded-md transition-all ${chartPeriod === "WEEK" ? 'bg-white shadow-sm text-indigo-600' : 'text-slate-500 hover:text-slate-800'}`}>주봉</button>
                            <button onClick={() => setChartPeriod("MONTH")} className={`px-4 py-1 text-xs font-bold rounded-md transition-all ${chartPeriod === "MONTH" ? 'bg-white shadow-sm text-indigo-600' : 'text-slate-500 hover:text-slate-800'}`}>월봉</button>
                          </div>
                        </div>
                        <GpuCandlestickChart 
                          gpuName={gpu.name} 
                          basePrice={lowestOffer.price_per_hour} 
                          exchangeRate={exchangeMultiplier} 
                          providers={gpu.offers.map(o => o.provider)} 
                          period={chartPeriod}
                        />
                      </div>
                    )}

                  </div>
                );
              })}
              
              {filteredAndSortedGpus.length === 0 && !loading && (
                <div className="py-24 text-center text-slate-500 flex flex-col items-center">
                  <div className="bg-slate-100 p-5 rounded-full mb-5 shadow-inner">
                    <Search size={36} className="text-slate-400" />
                  </div>
                  <p className="font-extrabold text-xl text-slate-700 mb-2 tracking-tight">검색 결과가 없습니다</p>
                  <p className="text-sm text-slate-500 font-medium">필터링을 조정하거나 다른 검색어를 입력해보세요.</p>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
