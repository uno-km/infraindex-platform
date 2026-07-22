"use client";

import React, { useState, useEffect } from 'react';
import { ShieldAlert, Play, Square, Settings, Database, Server, Clock, Search } from 'lucide-react';

interface CrawlerConfig {
  name: string;
  is_active: boolean;
  interval_minutes: number;
  target_urls: string | null;
}

export default function AdminDashboard() {
  const [crawlers, setCrawlers] = useState<CrawlerConfig[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isAdmin, setIsAdmin] = useState(false);
  
  // Mock login for demonstration
  const handleAdminLogin = () => {
    setIsAdmin(true);
    // In real app, fetch /auth/login/admin and store JWT
    // then fetch configs from /admin/config/crawlers
    setCrawlers([
      { name: "tier1_rss", is_active: true, interval_minutes: 60, target_urls: "https://feeds.bloomberg.com/technology/news.xml, https://hnrss.org/frontpage" },
      { name: "enterprise", is_active: false, interval_minutes: 120, target_urls: "https://www.dell.com/en-us/shop/servers-storage-and-networking/sc/servers" },
      { name: "orchestrator", is_active: true, interval_minutes: 30, target_urls: null }
    ]);
    setIsLoading(false);
  };

  const toggleCrawler = (name: string) => {
    setCrawlers(crawlers.map(c => 
      c.name === name ? { ...c, is_active: !c.is_active } : c
    ));
    // In real app, PUT /admin/config/crawlers/{name}
  };

  if (!isAdmin) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center p-4">
        <div className="bg-[#111] border border-red-500/30 p-8 rounded-xl max-w-md w-full">
          <div className="flex justify-center mb-6">
            <ShieldAlert className="w-16 h-16 text-red-500" />
          </div>
          <h1 className="text-2xl font-bold text-white text-center mb-6">System Override</h1>
          <p className="text-gray-400 text-sm text-center mb-8">
            Access restricted to Level 5 Clearance personnel.
          </p>
          <div className="space-y-4">
            <input 
              type="email" 
              placeholder="Admin Email" 
              className="w-full bg-[#050505] border border-gray-800 rounded px-4 py-3 text-white focus:outline-none focus:border-red-500 transition-colors"
            />
            <input 
              type="password" 
              placeholder="Password" 
              className="w-full bg-[#050505] border border-gray-800 rounded px-4 py-3 text-white focus:outline-none focus:border-red-500 transition-colors"
            />
            <button 
              onClick={handleAdminLogin}
              className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-3 px-4 rounded transition-colors"
            >
              Authenticate
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white p-8">
      <div className="max-w-7xl mx-auto">
        <header className="flex justify-between items-center mb-12">
          <div>
            <h1 className="text-3xl font-bold text-white flex items-center gap-3">
              <Database className="text-red-500" />
              Central Command
            </h1>
            <p className="text-gray-400 mt-2">Dynamic Config & Crawler Orchestration</p>
          </div>
          <div className="flex items-center gap-4">
            <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm font-medium border border-green-500/30 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
              Systems Nominal
            </span>
            <button className="p-2 hover:bg-gray-800 rounded transition-colors">
              <Settings className="w-5 h-5 text-gray-400" />
            </button>
          </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Panel */}
          <div className="lg:col-span-2 space-y-6">
            <h2 className="text-xl font-semibold flex items-center gap-2 mb-4">
              <Server className="w-5 h-5 text-blue-400" />
              Crawler Subsystems
            </h2>
            
            {crawlers.map((crawler) => (
              <div key={crawler.name} className="bg-[#111] border border-gray-800 p-6 rounded-xl shadow-lg">
                <div className="flex justify-between items-start mb-6">
                  <div>
                    <h3 className="text-lg font-bold text-white capitalize">{crawler.name.replace("_", " ")}</h3>
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
                  <div className="space-y-2">
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

          {/* Sidebar */}
          <div className="space-y-6">
            <div className="bg-[#111] border border-gray-800 p-6 rounded-xl">
              <h2 className="text-lg font-semibold mb-4">System Analytics</h2>
              <div className="space-y-4">
                <div className="flex justify-between items-center border-b border-gray-800 pb-2">
                  <span className="text-gray-400">Total Crawlers</span>
                  <span className="font-mono text-white">{crawlers.length}</span>
                </div>
                <div className="flex justify-between items-center border-b border-gray-800 pb-2">
                  <span className="text-gray-400">Active Tasks</span>
                  <span className="font-mono text-green-400">{crawlers.filter(c => c.is_active).length}</span>
                </div>
                <div className="flex justify-between items-center pb-2">
                  <span className="text-gray-400">Database Env</span>
                  <span className="px-2 py-1 bg-yellow-500/20 text-yellow-500 rounded text-xs font-bold border border-yellow-500/30">
                    DEV
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
