"use client";

import React, { useEffect, useState } from "react";
import { Server, Zap, HardDrive, Shield } from "lucide-react";

export default function EnterpriseDashboard() {
  const [hardware, setHardware] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/v1/retail/enterprise")
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setHardware(data);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch enterprise hardware:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-gold-500 animate-pulse">
        Initializing Secure Connection to Enterprise B2B Nodes...
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-in fade-in zoom-in duration-700">
      <div className="flex justify-between items-center mb-8 border-b border-gray-800 pb-4">
        <div>
          <h2 className="text-3xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-yellow-400 via-amber-500 to-yellow-600 drop-shadow-sm flex items-center gap-3">
            <Shield className="text-yellow-500 w-8 h-8" />
            Enterprise AI Infrastructure
          </h2>
          <p className="text-gray-400 text-sm mt-2 tracking-wide uppercase font-semibold">
            B2B Premium Hardware & Ultra High-End GPU Configurations
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
        {hardware.map((item, idx) => (
          <div
            key={idx}
            className="relative p-6 bg-black border border-gray-800 rounded-2xl hover:border-yellow-500/50 transition-all duration-300 shadow-2xl hover:shadow-yellow-500/10 group overflow-hidden"
          >
            {/* VIP Glow Effect */}
            <div className="absolute top-0 right-0 -mt-4 -mr-4 w-24 h-24 bg-yellow-500/10 rounded-full blur-2xl group-hover:bg-yellow-500/20 transition-all"></div>
            
            <div className="flex justify-between items-start mb-4 relative z-10">
              <span className="text-xs font-bold px-3 py-1.5 rounded-full bg-gradient-to-r from-gray-800 to-gray-900 border border-gray-700 text-yellow-500 uppercase tracking-widest shadow-inner">
                {item.platform}
              </span>
              {item.is_official && (
                <span className="text-[10px] text-green-400 border border-green-400/30 bg-green-400/10 px-2 py-1 rounded">
                  Official MSRP
                </span>
              )}
            </div>
            
            <h3 className="text-2xl font-bold text-white mb-6 relative z-10">
              {item.model_name}
            </h3>
            
            <div className="space-y-4 mb-6 relative z-10">
              <div className="flex items-center gap-3 text-gray-300 bg-gray-900/50 p-3 rounded-lg border border-gray-800/50">
                <HardDrive className="w-5 h-5 text-gray-500" />
                <span className="font-medium text-lg">
                  {item.capacity_gb} GB <span className="text-sm text-gray-500 font-normal">VRAM / System Memory</span>
                </span>
              </div>
            </div>

            <div className="mt-8 pt-6 border-t border-gray-800/80 flex justify-between items-end relative z-10">
              <div>
                <p className="text-xs text-gray-500 mb-1 uppercase tracking-wider font-semibold">Current Market Value</p>
                <div className="flex items-baseline gap-1">
                  <span className="text-yellow-500 font-bold text-2xl">$</span>
                  <span className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-b from-white to-gray-400">
                    {item.price.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 })}
                  </span>
                </div>
              </div>
              
              {item.url && (
                <a 
                  href={item.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="p-3 bg-yellow-500/10 text-yellow-500 rounded-xl hover:bg-yellow-500 hover:text-black transition-colors"
                  title="View Quote"
                >
                  <Zap className="w-5 h-5" />
                </a>
              )}
            </div>
          </div>
        ))}

        {hardware.length === 0 && (
          <div className="col-span-full flex flex-col items-center justify-center py-20 bg-black border border-gray-800 rounded-2xl">
            <Server className="w-16 h-16 text-gray-700 mb-4" />
            <p className="text-xl text-gray-500 font-semibold">No B2B hardware data available</p>
            <p className="text-sm text-gray-600 mt-2">Awaiting Enterprise Crawler execution...</p>
          </div>
        )}
      </div>
    </div>
  );
}
