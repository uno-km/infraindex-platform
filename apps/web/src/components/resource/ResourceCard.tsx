"use client";

import { useState } from "react";
import { Activity, HardDrive, Cpu, List, Info, ChevronRight, ExternalLink } from "lucide-react";
import ChartWidget from "./ChartWidget";

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

interface ResourceCardProps {
  item: ResourceModel;
  exchangeMultiplier: number;
  currencySymbol: string;
  formatPrice: (price: number) => string;
}

export default function ResourceCard({ item, exchangeMultiplier, currencySymbol, formatPrice }: ResourceCardProps) {
  const [isChartOpen, setIsChartOpen] = useState(false);
  const [isProvidersExpanded, setIsProvidersExpanded] = useState(false);
  const [chartPeriod, setChartPeriod] = useState<"DAY" | "WEEK" | "MONTH">("DAY");

  const sortedOffers = [...item.offers].sort((a, b) => a.price_per_hour - b.price_per_hour);
  const lowestOffer = sortedOffers[0];
  const highestOffer = sortedOffers[sortedOffers.length - 1];
  const avgPrice = sortedOffers.reduce((acc, curr) => acc + curr.price_per_hour, 0) / sortedOffers.length;

  const logTraffic = () => {
    fetch(`http://localhost:8000/api/v1/traffic/${item.id}`, { method: 'POST' }).catch(console.error);
  };

  const handleToggleChart = () => {
    if (!isChartOpen) logTraffic();
    setIsChartOpen(!isChartOpen);
  };

  const handleToggleProviders = () => {
    if (!isProvidersExpanded) logTraffic();
    setIsProvidersExpanded(!isProvidersExpanded);
  };

  return (
    <div className="p-8 flex flex-col hover:bg-slate-50/40 transition-colors duration-300 group">
      <div className="flex gap-8 w-full items-start">
        
        {/* Product Overview */}
        <div className="flex-1">
          <div className="flex items-center mb-3 gap-2">
            <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-md tracking-wider border border-emerald-100/50">즉시 할당 가능</span>
            {(item.popularity_score || 0) > 3 && (
              <span className="text-[10px] font-bold text-rose-600 bg-rose-50 px-2.5 py-1 rounded-md tracking-wider border border-rose-100/50 flex items-center">
                🔥 많이 찾음
              </span>
            )}
          </div>
          <h4 className="text-2xl font-black text-slate-900 leading-tight mb-2 tracking-tight">
            {item.name} {item.vram_gb ? <span className="text-slate-400 font-semibold text-lg ml-1 font-mono">({item.vram_gb}GB VRAM)</span> : null}
          </h4>
          
          <div className="text-sm text-slate-500 leading-relaxed mb-6 flex flex-wrap gap-x-5 gap-y-2 font-medium">
            <span className="flex items-center"><Activity size={14} className="mr-1.5 text-slate-400"/> AI 딥러닝 & 추론 최적화</span>
            {lowestOffer?.sys_ram_gb ? <span className="flex items-center"><HardDrive size={14} className="mr-1.5 text-slate-400"/> 시스템 RAM: {lowestOffer.sys_ram_gb}GB</span> : null}
            {lowestOffer?.tdp_w ? <span className="flex items-center"><Cpu size={14} className="mr-1.5 text-slate-400"/> TDP: {lowestOffer.tdp_w}W</span> : null}
          </div>

          <div className="flex items-center gap-3">
            <button 
              onClick={handleToggleChart}
              className={`border text-sm font-bold px-5 py-2.5 rounded-xl transition-all duration-200 flex items-center ${isChartOpen ? 'bg-indigo-600 text-white border-indigo-600 shadow-md shadow-indigo-200' : 'bg-white border-slate-200 text-slate-700 hover:border-slate-300 hover:bg-slate-50 shadow-sm'}`}
            >
              <Activity size={16} className={`mr-2 ${isChartOpen ? 'text-indigo-200' : 'text-indigo-500'}`} /> 
              {isChartOpen ? '차트 닫기' : '시세 변동표'}
            </button>
            
            <button 
              onClick={handleToggleProviders}
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
              onClick={() => logTraffic()}
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
            <div className="text-sm font-bold text-slate-700">시세 변동표</div>
            <div className="flex bg-slate-100 p-1 rounded-lg border border-slate-200/50">
              <button onClick={() => setChartPeriod("DAY")} className={`px-4 py-1 text-xs font-bold rounded-md transition-all ${chartPeriod === "DAY" ? 'bg-white shadow-sm text-indigo-600' : 'text-slate-500 hover:text-slate-800'}`}>일봉</button>
              <button onClick={() => setChartPeriod("WEEK")} className={`px-4 py-1 text-xs font-bold rounded-md transition-all ${chartPeriod === "WEEK" ? 'bg-white shadow-sm text-indigo-600' : 'text-slate-500 hover:text-slate-800'}`}>주봉</button>
              <button onClick={() => setChartPeriod("MONTH")} className={`px-4 py-1 text-xs font-bold rounded-md transition-all ${chartPeriod === "MONTH" ? 'bg-white shadow-sm text-indigo-600' : 'text-slate-500 hover:text-slate-800'}`}>월봉</button>
            </div>
          </div>
          <ChartWidget 
            gpuName={item.name} 
            basePrice={lowestOffer.price_per_hour} 
            exchangeRate={exchangeMultiplier} 
            providers={item.offers.map(o => o.provider)} 
            period={chartPeriod}
          />
        </div>
      )}

    </div>
  );
}
