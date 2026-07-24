"use client";

import { useState } from "react";
import GpuDashboard from "../components/GpuDashboard";
import { RetailDashboard } from "../components/RetailDashboard";
import InsightDashboard from "../components/InsightDashboard";
import NewsDashboard from "../components/NewsDashboard";
import EnterpriseDashboard from "../components/EnterpriseDashboard";
import StorageDashboard from "../components/StorageDashboard";
import TabButton from "../components/TabButton";
import { useAuth } from "../context/AuthContext";
import Header from "../components/layout/Header";
import Sidebar from "../components/layout/Sidebar";

export default function Home() {
  const [selectedCategory, setSelectedCategory] = useState<string>("gpu");
  const [searchQuery, setSearchQuery] = useState<string>("");

  // gpu/cpu/baremetal → GpuDashboard, storage → StorageDashboard
  const isGpuCategory = ["gpu", "cpu", "baremetal"].includes(selectedCategory);

  return (
    <div className="min-h-screen bg-slate-50/50 font-sans text-slate-900 pb-24 selection:bg-indigo-100">
      {/* Global Header */}
      <Header searchQuery={searchQuery} setSearchQuery={setSearchQuery} />

      {/* Main Layout Area */}
      <div className="max-w-7xl mx-auto mt-8 px-6 flex gap-8 items-start">
        {/* Global Sidebar */}
        <Sidebar selectedCategory={selectedCategory} setSelectedCategory={setSelectedCategory} />

        {/* Main Dynamic Content Area */}
        <main className="flex-1 min-w-0">
          {isGpuCategory && (
            <GpuDashboard selectedCategory={selectedCategory} searchQuery={searchQuery} />
          )}

          {selectedCategory === 'storage' && (
            <div className="animate-in fade-in zoom-in duration-500">
              <StorageDashboard />
            </div>
          )}

          {selectedCategory === 'retail' && (
            <div className="animate-in fade-in zoom-in duration-500">
              <RetailDashboard />
            </div>
          )}

          {selectedCategory === 'enterprise' && (
            <div className="animate-in fade-in zoom-in duration-500">
              <EnterpriseDashboard />
            </div>
          )}

          {selectedCategory === 'insights' && (
            <div className="animate-in fade-in zoom-in duration-500">
              <InsightDashboard />
            </div>
          )}

          {selectedCategory === 'news' && (
            <div className="animate-in fade-in zoom-in duration-500">
              <NewsDashboard />
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
