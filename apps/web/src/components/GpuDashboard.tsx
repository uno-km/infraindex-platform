"use client";

import { useEffect, useState, useMemo } from "react";
import { Search, Menu, User, Activity, Bookmark, ChevronRight, Server, Cpu, HardDrive, Cloud, Info } from "lucide-react";
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

const GpuCandlestickChart = ({ gpuName, basePrice, exchangeRate, providers }: { gpuName: string, basePrice: number, exchangeRate: number, providers: string[] }) => {
  const seriesData = useMemo(() => {
    const data = [];
    let currentPrice = basePrice;
    const now = new Date();
    
    for (let i = 30; i >= 0; i--) {
      const date = new Date(now.getTime() - i * 24 * 60 * 60 * 1000);
      const volatility = currentPrice * 0.05; 
      const open = currentPrice + (Math.random() - 0.5) * volatility;
      const close = open + (Math.random() - 0.5) * volatility;
      const high = Math.max(open, close) + Math.random() * volatility;
      const low = Math.min(open, close) - Math.random() * volatility;
      
      data.push({
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
      currentPrice = close;
    }
    return [{ data }];
  }, [basePrice, exchangeRate]);

  const currencySymbol = exchangeRate === 1 ? "$" : "₩";

  const options = {
    chart: { type: 'candlestick', toolbar: { show: false }, fontFamily: 'inherit', background: 'transparent' },
    title: { text: `${gpuName} Price Volatility (30 Days)`, align: 'left', style: { fontSize: '14px', fontWeight: '600', color: '#111827' } },
    xaxis: { type: 'datetime', labels: { style: { colors: '#6B7280' } } },
    yaxis: { 
      tooltip: { enabled: true }, 
      labels: { formatter: (val: number) => `${currencySymbol}${val.toLocaleString()}` } 
    },
    tooltip: {
      custom: function({seriesIndex, dataPointIndex, w}: any) {
        const data = w.globals.initialSeries[seriesIndex].data[dataPointIndex];
        const [o, h, l, c] = data.y;
        return `
          <div class="p-3 bg-white text-xs text-gray-800 shadow-xl border border-gray-200 rounded-lg min-w-[160px]">
            <div class="mb-2 font-bold text-gray-500 border-b border-gray-100 pb-1">${new Date(data.x).toLocaleDateString()}</div>
            <div class="mb-1 flex justify-between gap-4"><span>Open:</span> <strong>${currencySymbol}${o}</strong></div>
            <div class="mb-1 flex justify-between gap-4 text-red-600">
              <span class="truncate capitalize max-w-[80px]" title="Highest price reported by ${data.highProvider}">High (${data.highProvider}):</span> 
              <strong>${currencySymbol}${h}</strong>
            </div>
            <div class="mb-1 flex justify-between gap-4 text-blue-600">
              <span class="truncate capitalize max-w-[80px]" title="Lowest price reported by ${data.lowProvider}">Low (${data.lowProvider}):</span> 
              <strong>${currencySymbol}${l}</strong>
            </div>
            <div class="mt-1 flex justify-between gap-4 pt-1 border-t border-gray-100"><span>Close:</span> <strong>${currencySymbol}${c}</strong></div>
          </div>
        `;
      }
    },
    plotOptions: {
      candlestick: {
        colors: { upward: '#10b981', downward: '#ef4444' }, 
        wick: { useDataColors: true }
      }
    },
    grid: { borderColor: '#f3f4f6' }
  };

  return (
    <div className="bg-white p-5 rounded-lg border border-gray-200 mt-4 shadow-sm">
      <Chart options={options as any} series={seriesData} type="candlestick" height={250} />
    </div>
  );
};

export default function GpuDashboard() {
  const [gpus, setGpus] = useState<GpuModel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  
  const [selectedSeries, setSelectedSeries] = useState<string>("ALL");
  const [sortBy, setSortBy] = useState<"PRICE_ASC" | "VRAM_DESC">("PRICE_ASC");
  
  const [selectedChartGpu, setSelectedChartGpu] = useState<string | null>(null);

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
      if (g.name.includes("RTX")) seriesSet.add("RTX Series");
      else if (g.name.includes("A100") || g.name.includes("A10") || g.name.includes("A6000")) seriesSet.add("A Series");
      else if (g.name.includes("H100")) seriesSet.add("H Series");
      else if (g.name.includes("L40") || g.name.includes("L4")) seriesSet.add("L Series");
      else if (g.name.includes("V100")) seriesSet.add("V Series");
      else seriesSet.add("Other");
    });
    return ["ALL", ...Array.from(seriesSet)];
  }, [gpus]);

  const filteredAndSortedGpus = useMemo(() => {
    let result = gpus.filter(g => g.name.toLowerCase().includes(searchQuery.toLowerCase()));
    
    if (selectedSeries !== "ALL") {
      result = result.filter(g => {
        if (selectedSeries === "RTX Series") return g.name.includes("RTX");
        if (selectedSeries === "A Series") return g.name.includes("A100") || g.name.includes("A10") || g.name.includes("A6000");
        if (selectedSeries === "H Series") return g.name.includes("H100");
        if (selectedSeries === "L Series") return g.name.includes("L40") || g.name.includes("L4");
        if (selectedSeries === "V Series") return g.name.includes("V100");
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
    { icon: <Server size={18}/>, name: "GPU Instances", active: true },
    { icon: <Cpu size={18}/>, name: "CPU Computing" },
    { icon: <HardDrive size={18}/>, name: "Storage & Block" },
    { icon: <Cloud size={18}/>, name: "Baremetal Server" },
  ];

  if (loading) return <div className="h-screen flex items-center justify-center"><div className="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600"></div></div>;

  return (
    <div className="min-h-screen bg-gray-50 font-sans text-gray-900 pb-20">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto flex items-center justify-between py-4 px-6">
          <div className="flex items-center gap-8">
            <div className="text-2xl font-black text-indigo-700 tracking-tight cursor-pointer flex items-center">
              <Cloud className="mr-2" size={28} /> InfraIndex
              <span className="text-xs text-gray-400 font-medium ml-3 tracking-normal hidden md:inline-block border-l pl-3">Cloud Resources Exchange</span>
            </div>
          </div>

          <div className="flex-1 max-w-lg mx-8">
            <div className="relative flex items-center">
              <input 
                type="text" 
                placeholder="Search instances (e.g. H100, A100)" 
                className="w-full bg-gray-100 border-transparent focus:bg-white border-2 focus:border-indigo-500 rounded-lg py-2.5 px-4 text-sm outline-none transition-all"
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
              />
              <button className="absolute right-3 text-gray-400 hover:text-indigo-600">
                <Search size={20} />
              </button>
            </div>
          </div>

          <div className="flex gap-6 items-center text-gray-600">
            <div className="flex items-center gap-2 cursor-pointer hover:text-indigo-600 transition-colors">
              <Activity size={20} />
              <span className="text-sm font-medium hidden sm:block">Market Data</span>
            </div>
            <div className="flex items-center gap-2 cursor-pointer hover:text-indigo-600 transition-colors">
              <Bookmark size={20} />
              <span className="text-sm font-medium hidden sm:block">Watchlist</span>
            </div>
            <div className="flex items-center gap-2 cursor-pointer hover:text-indigo-600 transition-colors">
              <User size={20} />
              <span className="text-sm font-medium hidden sm:block">Sign In</span>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto mt-8 px-6 flex gap-8 items-start">
        
        <aside className="w-60 flex-shrink-0 bg-white border border-gray-200 rounded-xl overflow-hidden sticky top-[100px]">
          <div className="bg-gray-50 text-gray-700 py-4 px-5 flex items-center font-bold text-sm uppercase tracking-wider border-b border-gray-200">
            <Menu className="mr-2" size={18} /> Resource Types
          </div>
          <ul className="py-2">
            {categories.map((cat, idx) => (
              <li key={idx} className={`px-5 py-3 text-sm font-medium border-b border-gray-50 last:border-0 cursor-pointer flex justify-between items-center transition-colors ${cat.active ? 'bg-indigo-50 text-indigo-700 border-l-4 border-indigo-600' : 'text-gray-600 hover:bg-gray-50 hover:text-indigo-600'}`}>
                <span className="flex items-center gap-3">
                  <span className="text-gray-400">{cat.icon}</span>
                  {cat.name}
                </span>
                {cat.active && <ChevronRight size={16} />}
              </li>
            ))}
          </ul>
        </aside>

        <main className="flex-1 min-w-0">
          
          <div className="bg-white border border-gray-200 rounded-xl shadow-sm mb-6 p-5 flex justify-between items-center flex-wrap gap-4">
            <div className="flex items-center gap-3">
              <span className="font-bold text-sm text-gray-700">Filter:</span>
              <div className="flex gap-2 flex-wrap">
                {seriesOptions.map(series => (
                  <button 
                    key={series}
                    onClick={() => setSelectedSeries(series)}
                    className={`px-3 py-1.5 text-xs font-semibold rounded-md transition-colors border ${selectedSeries === series ? 'bg-indigo-600 text-white border-indigo-600 shadow-sm' : 'bg-white text-gray-600 border-gray-200 hover:bg-gray-50'}`}
                  >
                    {series}
                  </button>
                ))}
              </div>
            </div>
            
            <div className="flex items-center gap-4">
               <div className="flex bg-gray-100 p-1 rounded-lg">
                 <button 
                   onClick={() => setCurrency("USD")}
                   className={`px-3 py-1 text-xs font-bold rounded-md transition-colors ${currency === "USD" ? 'bg-white shadow text-gray-900' : 'text-gray-500 hover:text-gray-700'}`}
                 >
                   $ USD
                 </button>
                 <button 
                   onClick={() => setCurrency("KRW")}
                   className={`px-3 py-1 text-xs font-bold rounded-md transition-colors ${currency === "KRW" ? 'bg-white shadow text-gray-900' : 'text-gray-500 hover:text-gray-700'}`}
                 >
                   ₩ KRW
                 </button>
               </div>
               <select 
                 className="bg-white border border-gray-200 text-gray-700 text-sm rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none p-2 font-medium shadow-sm"
                 value={sortBy}
                 onChange={(e) => setSortBy(e.target.value as any)}
               >
                 <option value="PRICE_ASC">Lowest Price First</option>
                 <option value="VRAM_DESC">Highest VRAM First</option>
               </select>
            </div>
          </div>

          {error && <div className="bg-red-50 text-red-600 p-4 rounded-xl border border-red-200 mb-6 text-sm font-medium">{error}</div>}

          <div className="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
            <div className="border-b border-gray-200 px-6 py-4 flex justify-between items-center bg-gray-50/80">
              <h3 className="font-bold text-gray-900 flex items-center">
                <span className="w-2 h-2 rounded-full bg-green-500 mr-2 animate-pulse"></span>
                Global Cloud Instances Market
              </h3>
              <div className="text-sm text-gray-500 font-medium">Found <span className="text-indigo-600 font-bold">{filteredAndSortedGpus.length}</span> models</div>
            </div>

            <div className="divide-y divide-gray-100">
              {filteredAndSortedGpus.map((gpu) => {
                const sortedOffers = [...gpu.offers].sort((a, b) => a.price_per_hour - b.price_per_hour);
                const lowestOffer = sortedOffers[0];
                const highestOffer = sortedOffers[sortedOffers.length - 1];
                const avgPrice = sortedOffers.reduce((acc, curr) => acc + curr.price_per_hour, 0) / sortedOffers.length;
                
                const isChartOpen = selectedChartGpu === gpu.id;

                return (
                  <div key={gpu.id} className="p-6 flex flex-col hover:bg-gray-50/50 transition-colors group">
                    <div className="flex gap-6 w-full items-start">
                      
                      {/* Product Overview */}
                      <div className="flex-1">
                        <div className="flex items-center mb-2 gap-2">
                          <span className="text-[10px] font-bold text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded uppercase tracking-wider border border-indigo-100">Instantly Available</span>
                        </div>
                        <h4 className="text-xl font-bold text-gray-900 leading-tight mb-2">
                          {gpu.name} <span className="text-gray-400 font-medium text-lg ml-1">({gpu.vram_gb}GB VRAM)</span>
                        </h4>
                        
                        <div className="text-sm text-gray-500 leading-relaxed mb-4 flex flex-wrap gap-x-4 gap-y-1">
                          <span>• Optimal for Deep Learning</span>
                          {lowestOffer?.sys_ram_gb ? <span>• Rec. RAM: {lowestOffer.sys_ram_gb}GB</span> : null}
                          {lowestOffer?.tdp_w ? <span>• TDP: {lowestOffer.tdp_w}W</span> : null}
                        </div>

                        <div className="flex items-center gap-3">
                          <button 
                            onClick={() => setSelectedChartGpu(isChartOpen ? null : gpu.id)}
                            className={`border text-xs font-semibold px-4 py-2 rounded-lg transition-colors flex items-center ${isChartOpen ? 'bg-gray-900 text-white border-gray-900' : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-100 shadow-sm'}`}
                          >
                            <Activity size={14} className="mr-1.5" /> 
                            {isChartOpen ? 'Hide Market Data' : 'View Market Data'}
                          </button>
                        </div>
                      </div>

                      {/* Pricing Stats Column */}
                      <div className="w-64 bg-gray-50 rounded-xl p-4 border border-gray-100 group-hover:bg-white transition-colors relative">
                        <div className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-3 border-b border-gray-200 pb-2">Pricing Intel</div>
                        
                        <div className="space-y-3">
                          <div className="flex justify-between items-end group/tooltip relative">
                            <span className="text-sm font-medium text-gray-600 flex items-center">Lowest <Info size={12} className="ml-1 text-gray-400"/></span>
                            <span className="text-lg font-bold text-green-600">{formatPrice(lowestOffer?.price_per_hour || 0)}</span>
                            {/* Tooltip */}
                            <div className="absolute bottom-full left-0 mb-2 hidden group-hover/tooltip:block bg-gray-900 text-white text-xs px-3 py-2 rounded shadow-lg whitespace-nowrap z-10">
                              Provided by: <span className="font-bold capitalize">{lowestOffer?.provider}</span>
                            </div>
                          </div>

                          <div className="flex justify-between items-end group/tooltip relative">
                            <span className="text-sm font-medium text-gray-600 flex items-center">Average <Info size={12} className="ml-1 text-gray-400"/></span>
                            <span className="text-sm font-bold text-gray-700">{formatPrice(avgPrice)}</span>
                            <div className="absolute bottom-full left-0 mb-2 hidden group-hover/tooltip:block bg-gray-900 text-white text-xs px-3 py-2 rounded shadow-lg whitespace-nowrap z-10">
                              Calculated from {sortedOffers.length} global providers
                            </div>
                          </div>

                          <div className="flex justify-between items-end group/tooltip relative">
                            <span className="text-sm font-medium text-gray-600 flex items-center">Highest <Info size={12} className="ml-1 text-gray-400"/></span>
                            <span className="text-sm font-bold text-red-500">{formatPrice(highestOffer?.price_per_hour || 0)}</span>
                            <div className="absolute bottom-full left-0 mb-2 hidden group-hover/tooltip:block bg-gray-900 text-white text-xs px-3 py-2 rounded shadow-lg whitespace-nowrap z-10">
                              Provided by: <span className="font-bold capitalize">{highestOffer?.provider}</span>
                            </div>
                          </div>
                        </div>

                        {lowestOffer && (
                          <a 
                            href={lowestOffer.provider_link || "#"}
                            target="_blank"
                            rel="noopener noreferrer" 
                            className="mt-4 w-full bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold py-2.5 rounded-lg shadow-sm transition-colors flex items-center justify-center"
                          >
                            Deploy Lowest <ChevronRight size={16} className="ml-1 opacity-70" />
                          </a>
                        )}
                      </div>

                    </div>

                    {isChartOpen && lowestOffer && (
                      <div className="mt-5 pt-5 border-t border-gray-100 animate-in fade-in duration-300">
                        <GpuCandlestickChart gpuName={gpu.name} basePrice={lowestOffer.price_per_hour} exchangeRate={exchangeMultiplier} providers={gpu.offers.map(o => o.provider)} />
                      </div>
                    )}

                  </div>
                );
              })}
              
              {filteredAndSortedGpus.length === 0 && !loading && (
                <div className="py-24 text-center text-gray-500 flex flex-col items-center">
                  <div className="bg-gray-100 p-4 rounded-full mb-4">
                    <Search size={32} className="text-gray-400" />
                  </div>
                  <p className="font-bold text-lg text-gray-700 mb-1">No instances found</p>
                  <p className="text-sm">Adjust your filters or search query to find available hardware.</p>
                </div>
              )}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
