"use client";

import { useState } from "react";
import GpuDashboard from "../components/GpuDashboard";
import { RetailDashboard } from "../components/RetailDashboard";
import InsightDashboard from "../components/InsightDashboard";
import NewsDashboard from "../components/NewsDashboard";
import TabButton from "../components/TabButton";

export default function Home() {
  const [activeTab, setActiveTab] = useState("storage");

  return (
    <main className="min-h-screen p-8 relative overflow-hidden">
      {/* Background decorations */}
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-purple-600/20 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-blue-600/20 rounded-full blur-[120px] pointer-events-none" />

      <div className="max-w-7xl mx-auto relative z-10">
        <header className="flex justify-between items-end mb-12 animate-in fade-in slide-in-from-top-4 duration-700">
          <div>
            <h1 className="text-4xl font-bold tracking-tighter text-white mb-2">
              Infra<span className="text-neon">Index</span>
            </h1>
            <div className="flex gap-2">
              <TabButton id="storage" active={activeTab} onClick={setActiveTab}>Storage</TabButton>
              <TabButton id="retail" active={activeTab} onClick={setActiveTab}>Retail Market</TabButton>
              <TabButton id="insights" active={activeTab} onClick={setActiveTab}>Market Insights</TabButton>
              <TabButton id="news" active={activeTab} onClick={setActiveTab}>Global News</TabButton>
            </div>
          </div>
          <div className="text-right">
            <div className="inline-flex items-center gap-2 glass-panel px-4 py-2 rounded-full animate-pulse-glow">
              <span className="w-2 h-2 rounded-full bg-green-400"></span>
              <span className="text-xs text-green-400 font-medium tracking-wider uppercase">Live Network</span>
            </div>
          </div>
        </header>

        {activeTab === 'storage' && (
          <div className="space-y-6 animate-in fade-in zoom-in duration-500">
            <GpuDashboard />
          </div>
        )}

        {activeTab === 'retail' && (
          <div className="space-y-6 animate-in fade-in zoom-in duration-500">
            <RetailDashboard />
          </div>
        )}

        {activeTab === 'insights' && (
          <div className="space-y-6 animate-in fade-in zoom-in duration-500">
            <InsightDashboard />
          </div>
        )}

        {activeTab === 'news' && (
          <div className="space-y-6 animate-in fade-in zoom-in duration-500">
            <NewsDashboard />
          </div>
        )}
      </div>
    </main>
  );
}
