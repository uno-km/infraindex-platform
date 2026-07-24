"use client";

import { useEffect, useState, useMemo, useCallback } from "react";
import { Search, Activity, RefreshCw, HardDrive, Database } from "lucide-react";
import ResourceCard from "./resource/ResourceCard";
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

interface ResourceModel {
  id: string;
  name: string;
  vram_gb: number;
  popularity_score?: number;
  offers: Offer[];
}

interface ResourceDashboardProps {
  selectedCategory: string;
  searchQuery: string;
}

export default function ResourceDashboard({ selectedCategory, searchQuery }: ResourceDashboardProps) {
  const [resources, setResources] = useState<ResourceModel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // SPA State
  const [selectedSeries, setSelectedSeries] = useState<string>("전체보기");
  const [sortBy, setSortBy] = useState<"PROVIDERS_DESC" | "PRICE_ASC" | "VRAM_DESC">("PROVIDERS_DESC");

  // Currency State
  const [currency, setCurrency] = useState<"USD" | "KRW">("USD");
  const [krwRate, setKrwRate] = useState<number>(1380);

  // Storage Specific States
  const [syncing, setSyncing] = useState(false);
  const [syncResult, setSyncResult] = useState<string | null>(null);
  const [chartSeries, setChartSeries] = useState<any[]>([]);
  const [chartLoading, setChartLoading] = useState(false);

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
  const fetchResources = useCallback(async () => {
    setLoading(true);
    setError(null);
    setResources([]);
    setSelectedSeries("전체보기");
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const endpoint = selectedCategory === "gpu" ? "gpus" : selectedCategory;
      const res = await fetch(`${apiUrl}/api/v1/${endpoint}`);
      
      if (!res.ok) {
        throw new Error("API_ERROR");
      }
      const data = await res.json();
      setResources(data);
    } catch (err: any) {
      console.error("API fetch failed:", err);
      setError("서버에서 데이터를 가져오지 못했습니다. 백엔드 서버가 실행 중인지 확인해주세요.");
    } finally {
      setLoading(false);
    }
  }, [selectedCategory]);

  useEffect(() => {
    fetchResources();
  }, [fetchResources]);

  // Fetch Storage Historical Chart Data
  const fetchStorageChart = useCallback(async () => {
    if (selectedCategory !== "storage") return;
    setChartLoading(true);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/api/v1/chart/unified?hw_typ=storage&days=30`);
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          const series = data.slice(0, 6).map((s: any) => ({
            name: `${s.provider} - ${s.model_name}`,
            data: (s.data || []).map((pt: any) => ({
              x: new Date(pt.time).getTime(),
              y: pt.value,
            })),
          }));
          setChartSeries(series);
        } else {
          setChartSeries([]);
        }
      }
    } catch (e) {
      console.error("Storage chart fetch failed:", e);
    } finally {
      setChartLoading(false);
    }
  }, [selectedCategory]);

  useEffect(() => {
    fetchStorageChart();
  }, [fetchStorageChart]);

  // Global Storage Price Sync Trigger
  const handleStorageSync = async () => {
    setSyncing(true);
    setSyncResult(null);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/api/v1/chart/storage/sync-global`, {
        method: "POST",
      });
      const data = await res.json();
      setSyncResult(
        data.status === "success"
          ? `✅ ${data.inserted}개 가격 동기화 완료 (${data.providers}개 공급자)`
          : `❌ 오류: ${data.message}`
      );
      if (data.status === "success") {
        await fetchResources();
        await fetchStorageChart();
      }
    } catch (e) {
      setSyncResult("❌ 서버 연결 실패");
    } finally {
      setSyncing(false);
    }
  };

  const exchangeMultiplier = currency === "KRW" ? krwRate : 1;
  const currencySymbol = currency === "KRW" ? "₩" : "$";
  
  const formatPrice = (price: number) => {
    const val = price * exchangeMultiplier;
    if (selectedCategory === "storage") {
      // 스토리지의 경우 GB/월 단위 표현
      return currency === "KRW"
        ? `₩${(price * krwRate * 730).toLocaleString(undefined, { maximumFractionDigits: 1 })}/GB/월`
        : `$${(price * 730).toFixed(4)}/GB/월`;
    }
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
      } else if (selectedCategory === "storage") {
        if (r.name.toLowerCase().includes("ssd") || r.name.toLowerCase().includes("gp3")) seriesSet.add("SSD Storage");
        else if (r.name.toLowerCase().includes("object") || r.name.toLowerCase().includes("s3") || r.name.toLowerCase().includes("blob")) seriesSet.add("Object Storage");
        else seriesSet.add("HDD / Other");
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
        } else if (selectedCategory === "storage") {
          if (selectedSeries === "SSD Storage") return r.name.toLowerCase().includes("ssd") || r.name.toLowerCase().includes("gp3");
          if (selectedSeries === "Object Storage") return r.name.toLowerCase().includes("object") || r.name.toLowerCase().includes("s3") || r.name.toLowerCase().includes("blob");
          return !r.name.toLowerCase().includes("ssd") && !r.name.toLowerCase().includes("gp3") && !r.name.toLowerCase().includes("object") && !r.name.toLowerCase().includes("s3") && !r.name.toLowerCase().includes("blob");
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
  }, [resources, searchQuery, selectedSeries, sortBy, selectedCategory]);

  const chartOptions: ApexCharts.ApexOptions = {
    chart: { type: "line", height: 280, toolbar: { show: false }, background: "transparent" },
    stroke: { curve: "smooth", width: 2 },
    xaxis: { type: "datetime", labels: { style: { colors: "#94a3b8", fontSize: "11px" } } },
    yaxis: {
      labels: {
        formatter: (v: number) => currency === "KRW" ? `₩${v.toFixed(0)}` : `$${v.toFixed(4)}`,
        style: { colors: "#94a3b8" },
      },
    },
    tooltip: { x: { format: "MM/dd" } },
    legend: { position: "top", fontSize: "11px" },
    grid: { borderColor: "#f1f5f9" },
    colors: ["#6366f1", "#10b981", "#f59e0b", "#3b82f6", "#ef4444", "#8b5cf6"],
  };

  return (
    <div className="w-full animate-in fade-in zoom-in duration-500 space-y-6">
      {/* Storage Specific Real-time Control Panel */}
      {selectedCategory === "storage" && (
        <div className="bg-gradient-to-r from-indigo-50 to-indigo-100/50 border border-indigo-200/60 rounded-3xl p-5 px-6 flex justify-between items-center flex-wrap gap-4 shadow-sm">
          <div>
            <h3 className="font-extrabold text-indigo-900 flex items-center gap-2">
              <HardDrive className="w-5 h-5 text-indigo-600" />
              글로벌 스토리지 데이터 동기화 패널
            </h3>
            <p className="text-xs text-indigo-600 font-medium mt-1">
              전세계 20개 클라우드 스토리지 요율을 네이버/AWS 등 원격 서버로부터 정규 크롤링 및 실시간 환율을 반영하여 DB에 적재합니다.
            </p>
          </div>
          <div className="flex items-center gap-3">
            {syncResult && (
              <span className="text-xs font-bold text-indigo-700 bg-white border border-indigo-150 px-3 py-2 rounded-xl animate-fade-in">
                {syncResult}
              </span>
            )}
            <button
              onClick={handleStorageSync}
              disabled={syncing}
              className="flex items-center gap-2 px-4 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-xl transition-all disabled:opacity-50 shadow-sm"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${syncing ? "animate-spin" : ""}`} />
              {syncing ? "동기화 중..." : "가격 동기화"}
            </button>
          </div>
        </div>
      )}

      {/* Main Filter Toolbar */}
      <div className="bg-white/80 backdrop-blur-sm border border-slate-200/60 rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] p-5 px-6 flex justify-between items-center flex-wrap gap-4">
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
             <option value="VRAM_DESC">
               {selectedCategory === "cpu" ? "RAM 높은 순 정렬" : selectedCategory === "storage" ? "용량 높은 순 정렬" : "VRAM 높은 순 정렬"}
             </option>
           </select>
        </div>
      </div>

      {error && <div className="bg-rose-50 text-rose-600 p-5 rounded-2xl border border-rose-200 text-sm font-semibold flex items-center shadow-sm"><Activity className="mr-2" size={18}/> {error}</div>}

      {/* Resource Table Card */}
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

      {/* Storage Price History Chart */}
      {selectedCategory === "storage" && (
        <div className="bg-white border border-slate-200/60 rounded-3xl p-6 shadow-sm">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-base font-extrabold text-slate-900 flex items-center gap-2">
              <Database className="w-5 h-5 text-indigo-500" />
              스토리지 가격 변동 추이 (₩/GB/월)
            </h3>
            <button
              onClick={fetchStorageChart}
              className="flex items-center gap-1 text-xs text-slate-500 hover:text-indigo-600 font-semibold border border-slate-200 px-3 py-1.5 rounded-xl transition-all"
            >
              <RefreshCw className={`w-3 h-3 ${chartLoading ? "animate-spin" : ""}`} />
              새로고침
            </button>
          </div>

          {chartSeries.length > 0 ? (
            <Chart
              type="line"
              height={280}
              series={chartSeries}
              options={chartOptions}
            />
          ) : (
            <div className="h-40 flex flex-col items-center justify-center text-slate-400 border border-dashed border-slate-200 rounded-2xl">
              <p className="text-sm font-semibold text-slate-500">차트 데이터가 없습니다</p>
              <p className="text-xs text-slate-400 mt-1">상단의 가격 동기화를 완료하면 추이 조회가 가능합니다.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
