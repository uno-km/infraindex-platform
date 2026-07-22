"use client";

import { useEffect, useState } from "react";
import { Zap } from "lucide-react";

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

export default function GpuDashboard() {
  const [gpus, setGpus] = useState<GpuModel[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // UI States
  const [planType, setPlanType] = useState("ondemand"); // ondemand, spot, reserved
  const [timeUnit, setTimeUnit] = useState("hourly"); // hourly, daily, monthly

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

  if (loading) {
    return (
      <div className="flex justify-center items-center py-20">
        <div className="text-gray-500 font-semibold">데이터를 불러오는 중입니다...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-10 text-center text-red-600 bg-red-50 border border-red-200 mt-10 rounded">
        <h3 className="font-bold text-lg mb-2">서버 연결 오류</h3>
        <p>API 서버에 연결할 수 없습니다. 크롤링 서버가 실행 중인지 확인하세요.</p>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-12 font-sans">
      {/* Title */}
      <h1 className="text-3xl font-bold text-gray-900 mb-8">GPU 요금</h1>

      {/* Toggle Controls */}
      <div className="flex justify-between items-center mb-8">
        {/* Left Toggles */}
        <div className="inline-flex bg-white border border-gray-200 rounded-lg p-1 shadow-sm">
          <button 
            className={`px-4 py-2 text-sm font-semibold rounded-md transition-colors ${planType === 'ondemand' ? 'bg-white shadow border border-gray-200 text-gray-900' : 'text-gray-500 hover:text-gray-700'}`}
            onClick={() => setPlanType('ondemand')}
          >
            온디맨드
          </button>
          <button 
            className={`px-4 py-2 text-sm font-semibold rounded-md transition-colors text-gray-400 cursor-not-allowed`}
            disabled
          >
            스팟 (출시 예정)
          </button>
          <button 
            className={`px-4 py-2 text-sm font-semibold rounded-md transition-colors ${planType === 'reserved' ? 'bg-white shadow border border-gray-200 text-gray-900' : 'text-gray-500 hover:text-gray-700'}`}
            onClick={() => setPlanType('reserved')}
          >
            예약 인스턴스
          </button>
        </div>

        {/* Right Toggles */}
        <div className="inline-flex bg-white border border-gray-200 rounded-lg p-1 shadow-sm">
          <button 
            className={`px-4 py-2 text-sm font-semibold rounded-md transition-colors ${timeUnit === 'hourly' ? 'bg-white shadow border border-gray-200 text-gray-900' : 'text-gray-500 hover:text-gray-700'}`}
            onClick={() => setTimeUnit('hourly')}
          >
            시간당
          </button>
          <button 
            className={`px-4 py-2 text-sm font-semibold rounded-md transition-colors ${timeUnit === 'daily' ? 'bg-white shadow border border-gray-200 text-gray-900' : 'text-gray-500 hover:text-gray-700'}`}
            onClick={() => setTimeUnit('daily')}
          >
            일간
          </button>
          <button 
            className={`px-4 py-2 text-sm font-semibold rounded-md transition-colors ${timeUnit === 'monthly' ? 'bg-white shadow border border-gray-200 text-gray-900' : 'text-gray-500 hover:text-gray-700'}`}
            onClick={() => setTimeUnit('monthly')}
          >
            월간
          </button>
        </div>
      </div>

      {/* Status Text */}
      <div className="flex items-center text-[#00b050] font-bold text-sm mb-3">
        <Zap size={16} className="mr-1 fill-[#00b050]" />
        즉시 사용 가능
      </div>

      {/* Main Table */}
      <div className="bg-white border border-green-200 rounded-2xl overflow-hidden shadow-sm">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-gray-100 bg-gray-50/50">
              <th className="p-5 text-sm font-bold text-gray-700 w-1/4">공급사</th>
              <th className="p-5 text-sm font-bold text-gray-700 w-1/4">GPU 모델</th>
              <th className="p-5 text-sm font-bold text-gray-700 w-1/6">VRAM</th>
              <th className="p-5 text-sm font-bold text-gray-700 w-1/6">온디맨드 가격</th>
              <th className="p-5 w-1/6"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {gpus.flatMap(gpu => {
              const sortedOffers = [...gpu.offers].sort((a, b) => a.price_per_hour - b.price_per_hour);
              
              return sortedOffers.map((offer, idx) => {
                // Calculate price based on time unit
                let displayPrice = offer.price_per_hour;
                let unitSuffix = "/hr";
                
                if (timeUnit === 'daily') {
                  displayPrice = offer.price_per_hour * 24;
                  unitSuffix = "/day";
                } else if (timeUnit === 'monthly') {
                  displayPrice = offer.price_per_hour * 24 * 30;
                  unitSuffix = "/mo";
                }

                return (
                  <tr key={`${gpu.id}-${offer.provider}-${idx}`} className="hover:bg-gray-50/50 transition-colors">
                    <td className="p-5">
                      <div className="font-bold text-gray-900 capitalize text-sm">{offer.provider}</div>
                      <div className="text-xs text-gray-400 mt-1">
                        {offer.sys_ram_gb ? `RAM ${offer.sys_ram_gb}GB` : ''} 
                        {offer.tdp_w ? ` · ${offer.tdp_w}W` : ''}
                      </div>
                    </td>
                    <td className="p-5 font-semibold text-gray-800 text-sm">{gpu.name}</td>
                    <td className="p-5 text-gray-600 text-sm font-medium">{gpu.vram_gb}GB</td>
                    <td className="p-5 font-semibold text-gray-900 text-sm">
                      ${displayPrice.toFixed(3)}{unitSuffix}
                    </td>
                    <td className="p-5 text-right">
                      {offer.is_available ? (
                        <a 
                          href={offer.provider_link || "#"} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="inline-block bg-gray-900 hover:bg-black text-white text-sm font-bold px-6 py-2.5 rounded-full transition-colors"
                        >
                          시작하기
                        </a>
                      ) : (
                        <span className="inline-block bg-gray-100 text-gray-400 text-sm font-bold px-6 py-2.5 rounded-full">
                          품절
                        </span>
                      )}
                    </td>
                  </tr>
                );
              });
            })}
            
            {gpus.length === 0 && (
              <tr>
                <td colSpan={5} className="py-10 text-center text-gray-500">
                  데이터가 없습니다.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
