"use client";

import { useEffect, useState } from "react";
import { Search } from "lucide-react";

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
  const [searchTerm, setSearchTerm] = useState("");

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
        <p>API 서버({process.env.NEXT_PUBLIC_API_URL || "localhost:8000"})에 연결할 수 없습니다.</p>
      </div>
    );
  }

  // 검색 필터링
  const filteredGpus = gpus.filter(g => 
    g.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
    g.offers.some(o => o.provider.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Header Section */}
      <div className="mb-6 pb-4 border-b-2 border-gray-800 flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">실시간 GPU 클라우드 가격비교</h1>
          <p className="text-sm text-gray-500 mt-1">글로벌 공급자(Vast.ai, RunPod 등)의 최저가를 확인하세요.</p>
        </div>
        
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={16} />
          <input 
            type="text" 
            placeholder="GPU 모델명 검색 (예: 4090)" 
            className="border border-gray-300 rounded px-3 py-1.5 pl-9 text-sm focus:outline-none focus:border-brand-blue focus:ring-1 focus:ring-brand-blue w-64"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {/* Main Table */}
      <div className="bg-white border border-gray-200 shadow-sm">
        <table className="data-table">
          <thead>
            <tr>
              <th className="w-32">공급사</th>
              <th className="text-left w-64">GPU 모델명</th>
              <th>VRAM</th>
              <th>시스템 RAM</th>
              <th>소비전력(TDP)</th>
              <th className="text-right">시간당 단가</th>
              <th className="w-32">구매/대여</th>
            </tr>
          </thead>
          <tbody>
            {filteredGpus.flatMap(gpu => {
              // Sort offers by price ascending
              const sortedOffers = [...gpu.offers].sort((a, b) => a.price_per_hour - b.price_per_hour);
              
              return sortedOffers.map((offer, idx) => (
                <tr key={`${gpu.id}-${offer.provider}-${idx}`}>
                  <td className="font-bold text-brand-blue capitalize">{offer.provider}</td>
                  <td className="text-left font-semibold text-gray-800">{gpu.name}</td>
                  <td className="text-gray-600">{gpu.vram_gb} GB</td>
                  <td className="text-gray-600">{offer.sys_ram_gb ? `${offer.sys_ram_gb} GB` : '-'}</td>
                  <td className="text-gray-600">{offer.tdp_w ? `${offer.tdp_w} W` : '-'}</td>
                  <td className="text-right font-bold text-brand-red text-base">
                    ${offer.price_per_hour.toFixed(3)}
                  </td>
                  <td>
                    {offer.is_available ? (
                      <a 
                        href={offer.provider_link || "#"} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="btn-rent"
                      >
                        대여하기 &gt;
                      </a>
                    ) : (
                      <span className="text-gray-400 text-xs font-bold bg-gray-100 px-2 py-1 rounded">품절</span>
                    )}
                  </td>
                </tr>
              ));
            })}
            
            {filteredGpus.length === 0 && (
              <tr>
                <td colSpan={7} className="py-10 text-gray-500">검색 결과가 없습니다.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
