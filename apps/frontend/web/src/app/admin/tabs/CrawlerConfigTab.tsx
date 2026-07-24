"use client";

import React, { useState, useEffect } from 'react';
import { Clock, Play, Square, Server } from 'lucide-react';
import { useAuth } from '../../../context/AuthContext';

interface CrawlerConfig {
  name: string;
  is_active: boolean;
  interval_minutes: number;
  target_urls: string | null;
}

export default function CrawlerConfigTab() {
  const { token } = useAuth();
  const [crawlers, setCrawlers] = useState<CrawlerConfig[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!token) return;
    
    const fetchConfigs = async () => {
      try {
        const res = await fetch('/api/v1/admin/config/crawlers', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setCrawlers(data);
        } else if (res.status === 404) {
          // fallback if endpoint not found for some reason, use mock data
          setCrawlers([
            { name: "gpu_data_crawling", is_active: true, interval_minutes: 60, target_urls: null }
          ]);
        }
      } catch (e) {
        console.error(e);
      } finally {
        setIsLoading(false);
      }
    };
    fetchConfigs();
  }, [token]);

  const toggleCrawler = (name: string) => {
    // In real app, call PUT endpoint. For now just update UI
    setCrawlers(crawlers.map(c => 
      c.name === name ? { ...c, is_active: !c.is_active } : c
    ));
  };

  if (isLoading) return <div className="text-gray-400">Loading configurations...</div>;

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold flex items-center gap-2 mb-4 text-white">
        <Server className="w-5 h-5 text-blue-400" />
        Crawler Subsystems Config
      </h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {crawlers.map((crawler) => (
          <div key={crawler.name} className="bg-[#1a1a1a] border border-gray-800 p-6 rounded-xl shadow-lg">
            <div className="flex justify-between items-start mb-6">
              <div>
                <h3 className="text-lg font-bold text-white capitalize">{crawler.name.replace(/_/g, " ")}</h3>
                <div className="flex items-center gap-4 mt-2 text-sm text-gray-400">
                  <span className="flex items-center gap-1">
                    <Clock className="w-4 h-4" /> {crawler.interval_minutes} min
                  </span>
                </div>
              </div>
              <button 
                onClick={() => toggleCrawler(crawler.name)}
                className={`px-4 py-2 rounded-lg font-medium flex items-center gap-2 transition-colors ${
                  crawler.is_active 
                    ? 'bg-red-500/10 text-red-500 hover:bg-red-500/20' 
                    : 'bg-green-500/10 text-green-500 hover:bg-green-500/20'
                }`}
              >
                {crawler.is_active ? <><Square className="w-4 h-4 fill-current"/> Suspend</> : <><Play className="w-4 h-4 fill-current"/> Engage</>}
              </button>
            </div>
            
            {crawler.target_urls !== null && (
              <div className="space-y-2 mt-4">
                <label className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Target URLs</label>
                <textarea 
                  className="w-full bg-[#050505] border border-gray-800 rounded p-3 text-sm text-gray-300 focus:outline-none focus:border-blue-500 font-mono"
                  rows={3}
                  defaultValue={crawler.target_urls}
                />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
