"use client";

import React, { useState } from 'react';
import { ShieldAlert, Database, RefreshCw, Users, Server, Table } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import CrawlerConfigTab from './tabs/CrawlerConfigTab';
import UsersTab from './tabs/UsersTab';
import DataViewerTab from './tabs/DataViewerTab';
import Link from 'next/link';

export default function AdminDashboard() {
  const { user, isAuthenticated, isLoading } = useAuth();
  const [activeTab, setActiveTab] = useState('crawlers');
  const [isRefreshing, setIsRefreshing] = useState(false);

  if (isLoading) {
    return <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center text-white font-mono animate-pulse">Loading System...</div>;
  }

  if (!isAuthenticated || !user?.is_admin) {
    return (
      <div className="min-h-screen bg-[#0a0a0a] flex items-center justify-center p-4">
        <div className="bg-[#111] border border-red-500/30 p-8 rounded-2xl max-w-md w-full shadow-2xl shadow-red-500/10">
          <div className="flex justify-center mb-6">
            <ShieldAlert className="w-16 h-16 text-red-500 drop-shadow-[0_0_15px_rgba(239,68,68,0.5)] animate-pulse" />
          </div>
          <h1 className="text-2xl font-bold text-white text-center mb-6">Access Denied</h1>
          <p className="text-gray-400 text-sm text-center mb-8">
            Access restricted to Level 5 Clearance personnel.
          </p>
          <Link href="/" className="block text-center text-indigo-400 hover:text-indigo-300 hover:underline font-semibold transition-colors">
            Return to Base
          </Link>
        </div>
      </div>
    );
  }

  const refreshSchedules = async () => {
    setIsRefreshing(true);
    try {
      const res = await fetch('/api/v1/admin/schedules/refresh', { method: 'POST' });
      if (res.ok) alert('Batch schedules refreshed successfully from DB to Singleton memory!');
      else alert('Failed to refresh schedules.');
    } catch (e) {
      alert('Error refreshing schedules.');
    } finally {
      setIsRefreshing(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white p-4 sm:p-8 selection:bg-indigo-500/30">
      <div className="max-w-7xl mx-auto">
        <header className="flex flex-col md:flex-row md:justify-between items-start md:items-center mb-10 gap-6 border-b border-gray-800 pb-8">
          <div>
            <h1 className="text-3xl font-black text-white flex items-center gap-3">
              <Database className="text-red-500 w-8 h-8" />
              Central Command
            </h1>
            <p className="text-gray-400 mt-2 font-medium">Welcome back, Commander <span className="text-indigo-400 font-bold">{user.nickname}</span></p>
          </div>
          <div className="flex flex-wrap items-center gap-4">
            <span className="px-3 py-1.5 bg-green-500/10 text-green-400 rounded-full text-xs font-bold border border-green-500/20 flex items-center gap-2 shadow-inner">
              <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></span>
              Systems Nominal
            </span>
            <button 
              onClick={refreshSchedules}
              disabled={isRefreshing}
              className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-800/50 text-white font-bold rounded-xl flex items-center gap-2 transition-all shadow-lg hover:shadow-indigo-500/20 active:scale-95"
            >
              <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
              Reload Schedules
            </button>
            <Link href="/" className="px-5 py-2.5 bg-[#111] border border-gray-800 hover:bg-[#222] rounded-xl transition-colors text-sm font-bold text-gray-300">
              Exit Admin
            </Link>
          </div>
        </header>

        {/* Tabs Navigation */}
        <div className="flex flex-wrap gap-3 mb-8 bg-[#111] p-2 rounded-2xl border border-gray-800 w-fit">
          <button 
            onClick={() => setActiveTab('crawlers')}
            className={`px-5 py-2.5 rounded-xl font-bold flex items-center gap-2 transition-all duration-300 ${activeTab === 'crawlers' ? 'bg-indigo-600 text-white shadow-md shadow-indigo-900/50' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}
          >
            <Server className="w-4 h-4" /> Crawler Config
          </button>
          <button 
            onClick={() => setActiveTab('users')}
            className={`px-5 py-2.5 rounded-xl font-bold flex items-center gap-2 transition-all duration-300 ${activeTab === 'users' ? 'bg-indigo-600 text-white shadow-md shadow-indigo-900/50' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}
          >
            <Users className="w-4 h-4" /> Users & Logs
          </button>
          <button 
            onClick={() => setActiveTab('data')}
            className={`px-5 py-2.5 rounded-xl font-bold flex items-center gap-2 transition-all duration-300 ${activeTab === 'data' ? 'bg-indigo-600 text-white shadow-md shadow-indigo-900/50' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}
          >
            <Table className="w-4 h-4" /> Data Viewer
          </button>
        </div>

        {/* Tab Content Panel */}
        <div className="bg-[#111] rounded-3xl p-6 md:p-8 border border-gray-800 shadow-2xl relative overflow-hidden group">
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-indigo-500 to-transparent opacity-50"></div>
          {activeTab === 'crawlers' && <CrawlerConfigTab />}
          {activeTab === 'users' && <UsersTab />}
          {activeTab === 'data' && <DataViewerTab />}
        </div>
      </div>
    </div>
  );
}
