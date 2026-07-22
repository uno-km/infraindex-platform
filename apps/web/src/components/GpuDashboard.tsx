"use client";

import { useEffect, useState, useMemo } from "react";
import { Search, Activity } from "lucide-react";
import Header from "./layout/Header";
import Sidebar from "./layout/Sidebar";
import ResourceCard from "./resource/ResourceCard";

interface Offer {
  provider: string;
  price_per_hour: number;
  is_available: boolean;
  region: string;
  provider_link?: string;
  sys_ram_gb?: number;
  tdp_w?: number;
}

interface ResourceModel {
  id: string;
  name: string;
  vram_gb: number;
  popularity_score?: number;
  offers: Offer[];
}

export default function GpuDashboard() {
  const [resources, setResources] = useState<ResourceModel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // SPA State
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("gpu");
  const [selectedSeries, setSelectedSeries] = useState<string>("전체보기");
  const [sortBy, setSortBy] = useState<"PROVIDERS_DESC" | "PRICE_ASC" | "VRAM_DESC">("PROVIDERS_DESC");

  // Currency State
  const [currency, setCurrency] = useState<"USD" | "KRW">("USD");
  const [krwRate, setKrwRate] = useState<number>(1);

  // Fetch Exchange Rate once
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
  }, []);

  // Fetch Resources when Category changes
  useEffect(() => {
    async function fetchResources() {
      setLoading(true);
      setError(null);
      setResources([]);
      setSelectedSeries("전체보기");
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        // Convert category to backend endpoint
        const endpoint = selectedCategory === "gpu" ? "gpus" : selectedCategory;
        const res = await fetch(`${apiUrl}/api/v1/${endpoint}`);
        
        if (!res.ok) throw new Error("데이터를 불러오는데 실패했습니다.");
        const data = await res.json();
        setResources(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchResources();
  }, [selectedCategory]);

  const exchangeMultiplier = currency === "KRW" ? krwRate : 1;
  const currencySymbol = currency === "KRW" ? "₩" : "$";
  const formatPrice = (price: number) => {
    const val = price * exchangeMultiplier;
    return currency === "KRW" 
      ? `₩${val.toLocaleString(undefined, { maximumFractionDigits: 0 })}` 
      : `$${val.toFixed(3)}`;
  };

  const seriesOptions = useMemo(() => {
    const seriesSet = new Set<string>();
    resources.forEach(r => {
      if (selectedCategory === "gpu") {
        if (r.name.includes("RTX")) seriesSet.add("RTX 시리즈");
        else if (r.name.includes("A100") || r.name.includes("A10") || r.name.includes("A6000")) seriesSet.add("A 시리즈");
        else if (r.name.includes("H100")) seriesSet.add("H 시리즈");
        else if (r.name.includes("L40") || r.name.includes("L4")) seriesSet.add("L 시리즈");
        else if (r.name.includes("V100")) seriesSet.add("V 시리즈");
        else seriesSet.add("기타");
      } else if (selectedCategory === "cpu") {
        if (r.name.includes("Xeon")) seriesSet.add("Intel Xeon");
        else if (r.name.includes("EPYC")) seriesSet.add("AMD EPYC");
        else if (r.name.includes("Core") || r.name.includes("i9") || r.name.includes("i7")) seriesSet.add("Intel Core");
        else if (r.name.includes("Ryzen")) seriesSet.add("AMD Ryzen");
        else seriesSet.add("기타");
      }
    });
    return ["전체보기", ...Array.from(seriesSet)];
  }, [resources, selectedCategory]);

  const filteredAndSortedResources = useMemo(() => {
    let result = resources.filter(r => r.name.toLowerCase().includes(searchQuery.toLowerCase()));
    
    if (selectedSeries !== "전체보기") {
      result = result.filter(r => {
        if (selectedCategory === "gpu") {
          if (selectedSeries === "RTX 시리즈") return r.name.includes("RTX");
          if (selectedSeries === "A 시리즈") return r.name.includes("A100") || r.name.includes("A10") || r.name.includes("A6000");
          if (selectedSeries === "H 시리즈") return r.name.includes("H100");
          if (selectedSeries === "L 시리즈") return r.name.includes("L40") || r.name.includes("L4");
          if (selectedSeries === "V 시리즈") return r.name.includes("V100");
          return !r.name.includes("RTX") && !r.name.includes("A100") && !r.name.includes("H100") && !r.name.includes("L40") && !r.name.includes("V100");
        } else if (selectedCategory === "cpu") {
          if (selectedSeries === "Intel Xeon") return r.name.includes("Xeon");
          if (selectedSeries === "AMD EPYC") return r.name.includes("EPYC");
          if (selectedSeries === "Intel Core") return r.name.includes("Core") || r.name.includes("i9") || r.name.includes("i7");
          if (selectedSeries === "AMD Ryzen") return r.name.includes("Ryzen");
          return !r.name.includes("Xeon") && !r.name.includes("EPYC") && !r.name.includes("Core") && !r.name.includes("Ryzen") && !r.name.includes("i9") && !r.name.includes("i7");
        }
        return true;
      });
    }

    result.sort((a, b) => {
      const minPriceA = Math.min(...a.offers.map(o => o.price_per_hour));
      const minPriceB = Math.min(...b.offers.map(o => o.price_per_hour));
      
      if (sortBy === "PROVIDERS_DESC") return b.offers.length - a.offers.length;
      if (sortBy === "PRICE_ASC") return minPriceA - minPriceB;
      if (sortBy === "VRAM_DESC") return b.vram_gb - a.vram_gb;
      return 0;
    });

    return result;
  }, [resources, searchQuery, selectedSeries, sortBy]);

  return (
    <div className="min-h-screen bg-slate-50/50 font-sans text-slate-900 pb-24 selection:bg-indigo-100">
      <Header searchQuery={searchQuery} setSearchQuery={setSearchQuery} />

      <div className="max-w-7xl mx-auto mt-8 px-6 flex gap-8 items-start">
        <Sidebar selectedCategory={selectedCategory} setSelectedCategory={setSelectedCategory} />

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
                 <option value="PROVIDERS_DESC">🔥 판매처 많은 순 정렬</option>
                 <option value="PRICE_ASC">최저가 순 정렬</option>
                 <option value="VRAM_DESC">{selectedCategory === "cpu" ? "RAM 높은 순 정렬" : "VRAM 높은 순 정렬"}</option>
               </select>
            </div>
          </div>

          {error && <div className="bg-rose-50 text-rose-600 p-5 rounded-2xl border border-rose-200 mb-6 text-sm font-semibold flex items-center shadow-sm"><Activity className="mr-2" size={18}/> {error}</div>}

          <div className="bg-white border border-slate-200/60 rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] overflow-hidden">
            <div className="border-b border-slate-100 px-8 py-5 flex justify-between items-center bg-white">
              <h3 className="font-extrabold text-slate-900 flex items-center text-lg capitalize">
                <span className="relative flex h-3 w-3 mr-3">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
                </span>
                글로벌 {selectedCategory.toUpperCase()} 인스턴스 시세표
              </h3>
              <div className="text-sm text-slate-500 font-medium bg-slate-50 px-3 py-1 rounded-lg border border-slate-100">총 검색 결과: <span className="text-indigo-600 font-bold">{filteredAndSortedResources.length}</span> 건</div>
            </div>

            <div className="divide-y divide-slate-100/80 relative min-h-[400px]">
              {loading && (
                <div className="absolute inset-0 bg-white/60 backdrop-blur-sm z-10 flex items-center justify-center">
                  <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600"></div>
                </div>
              )}

              {filteredAndSortedResources.map((resource) => (
                <ResourceCard 
                  key={resource.id} 
                  item={resource} 
                  selectedCategory={selectedCategory}
                  exchangeMultiplier={exchangeMultiplier} 
                  currencySymbol={currencySymbol} 
                  formatPrice={formatPrice} 
                />
              ))}
              
              {filteredAndSortedResources.length === 0 && !loading && (
                <div className="py-24 text-center text-slate-500 flex flex-col items-center">
                  <div className="bg-slate-100 p-5 rounded-full mb-5 shadow-inner">
                    <Search size={36} className="text-slate-400" />
                  </div>
                  <p className="font-extrabold text-xl text-slate-700 mb-2 tracking-tight">검색 결과가 없습니다</p>
                  <p className="text-sm text-slate-500 font-medium">선택하신 카테고리에 데이터가 없거나 필터링 조건에 맞지 않습니다.</p>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
