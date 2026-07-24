"use client";

import React, { useEffect, useState } from "react";
import { Server, Zap, HardDrive, Shield } from "lucide-react";

export default function EnterpriseDashboard() {
  const [hardware, setHardware] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/v1/retail/enterprise")
      .then((res) => {
        if (!res.ok) throw new Error("API_ERROR");
        return res.json();
      })
      .then((data) => {
        if (Array.isArray(data)) {
          setHardware(data);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error("Enterprise API failed:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-indigo-500 animate-pulse">
        Initializing Secure Connection to Enterprise B2B Nodes...
      </div>
    );
  }

  return (
    <div className="bg-white border border-slate-200/60 rounded-3xl p-6 w-full shadow-[0_8px_30px_rgb(0,0,0,0.04)] animate-in fade-in zoom-in duration-700">
      <div className="flex justify-between items-center mb-8 border-b border-slate-100 pb-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-3">
            <Shield className="text-indigo-600 w-8 h-8" />
            엔터프라이즈 AI 인프라
          </h2>
          <p className="text-slate-500 text-sm mt-2 font-medium">
            B2B 프리미엄 하드웨어 및 초고사양 GPU 구성
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
        {hardware.map((item, idx) => (
          <div
            key={idx}
            className="relative p-6 bg-white border border-slate-200 rounded-2xl hover:border-indigo-300 transition-all duration-300 shadow-sm hover:shadow-md group overflow-hidden"
          >
            {/* VIP Glow Effect */}
            <div className="absolute top-0 right-0 -mt-4 -mr-4 w-24 h-24 bg-indigo-50 rounded-full blur-2xl group-hover:bg-indigo-100 transition-all"></div>
            
            <div className="flex justify-between items-start mb-4 relative z-10">
              <span className="text-xs font-bold px-3 py-1.5 rounded-full bg-slate-50 border border-slate-200 text-indigo-700 uppercase tracking-widest">
                {item.platform}
              </span>
              {item.is_official && (
                <span className="text-[10px] text-emerald-600 border border-emerald-200 bg-emerald-50 px-2 py-1 rounded font-bold">
                  Official MSRP
                </span>
              )}
            </div>
            
            <h3 className="text-2xl font-bold text-slate-800 mb-6 relative z-10">
              {item.model_name}
            </h3>
            
            <div className="space-y-4 mb-6 relative z-10">
              <div className="flex items-center gap-3 text-slate-600 bg-slate-50 p-3 rounded-lg border border-slate-100">
                <HardDrive className="w-5 h-5 text-slate-400" />
                <span className="font-semibold text-lg">
                  {item.capacity_gb} GB <span className="text-sm text-slate-400 font-normal">VRAM / System Memory</span>
                </span>
              </div>
            </div>

            <div className="mt-8 pt-6 border-t border-slate-100 flex justify-between items-end relative z-10">
              <div>
                <p className="text-xs text-slate-500 mb-1 uppercase tracking-wider font-semibold">현재 시장가</p>
                <div className="flex items-baseline gap-1">
                  <span className="text-slate-400 font-bold text-2xl">$</span>
                  <span className="text-4xl font-black text-slate-800">
                    {item.price.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 })}
                  </span>
                </div>
              </div>
              
              {item.url && (
                <a 
                  href={item.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="p-3 bg-indigo-50 text-indigo-600 rounded-xl hover:bg-indigo-600 hover:text-white transition-colors shadow-sm"
                  title="View Quote"
                >
                  <Zap className="w-5 h-5" />
                </a>
              )}
            </div>
          </div>
        ))}

        {hardware.length === 0 && (
          <div className="col-span-full flex flex-col items-center justify-center py-24 text-center text-slate-500 bg-white border border-slate-200 rounded-2xl">
            <div className="bg-slate-50 p-5 rounded-full mb-5">
              <Server className="w-10 h-10 text-slate-400" />
            </div>
            <p className="font-extrabold text-xl text-slate-700 mb-2">B2B 하드웨어 데이터가 없습니다</p>
            <p className="text-sm text-slate-500 font-medium">엔터프라이즈 크롤러의 실행을 대기 중이거나 데이터가 없습니다.</p>
          </div>
        )}
      </div>
    </div>
  );
}
