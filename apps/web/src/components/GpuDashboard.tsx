"use client";

import { useEffect, useState } from "react";
import { Server, Activity, Zap, Cpu, Search, TrendingDown } from "lucide-react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

interface Offer {
  provider: string;
  price_per_hour: number;
  is_available: boolean;
  region: string;
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
        const res = await fetch("http://localhost:8000/api/v1/gpus");
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
      <div className="flex justify-center items-center h-64">
        <div className="w-12 h-12 border-4 border-[var(--color-cyber-purple)] border-t-[var(--color-cyber-neon)] rounded-full animate-spin"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass-panel p-6 text-red-400 border-red-500/30 rounded-xl text-center">
        <Server className="mx-auto mb-4 opacity-50" size={32} />
        <h3 className="text-xl mb-2">Connection Error</h3>
        <p className="opacity-80">Could not connect to the API server at localhost:8000. Is it running?</p>
      </div>
    );
  }

  const filteredGpus = gpus.filter(g => g.name.toLowerCase().includes(searchTerm.toLowerCase()));
  const totalOffers = gpus.reduce((acc, gpu) => acc + gpu.offers.length, 0);
  const providers = new Set(gpus.flatMap(g => g.offers.map(o => o.provider)));

  // Prepare chart data (Top 5 GPUs by offer count)
  const chartData = [...gpus]
    .sort((a, b) => b.offers.length - a.offers.length)
    .slice(0, 5)
    .map(g => ({
      name: g.name.replace("NVIDIA ", "").replace("GeForce ", ""), // Shorten name
      offers: g.offers.length,
    }));

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      {/* Top Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="glass-panel p-6 rounded-xl hover:-translate-y-1 transition-transform relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-32 h-32 bg-[var(--color-cyber-neon)]/10 rounded-full blur-2xl group-hover:bg-[var(--color-cyber-neon)]/20 transition-all"></div>
          <div className="flex justify-between items-start mb-4 relative z-10">
            <h3 className="text-gray-400 uppercase tracking-widest text-xs font-semibold">Tracked GPUs</h3>
            <Cpu className="text-neon opacity-70" size={20} />
          </div>
          <div className="text-4xl font-bold text-white relative z-10">{gpus.length}</div>
        </div>
        
        <div className="glass-panel p-6 rounded-xl hover:-translate-y-1 transition-transform relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-32 h-32 bg-[var(--color-cyber-purple)]/10 rounded-full blur-2xl group-hover:bg-[var(--color-cyber-purple)]/20 transition-all"></div>
          <div className="flex justify-between items-start mb-4 relative z-10">
            <h3 className="text-gray-400 uppercase tracking-widest text-xs font-semibold">Active Offers</h3>
            <Activity className="text-purple-glow opacity-70" size={20} />
          </div>
          <div className="text-4xl font-bold text-white relative z-10">{totalOffers}</div>
        </div>

        <div className="glass-panel p-6 rounded-xl hover:-translate-y-1 transition-transform relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-32 h-32 bg-[var(--color-cyber-accent)]/10 rounded-full blur-2xl group-hover:bg-[var(--color-cyber-accent)]/20 transition-all"></div>
          <div className="flex justify-between items-start mb-4 relative z-10">
            <h3 className="text-gray-400 uppercase tracking-widest text-xs font-semibold">Providers</h3>
            <Zap className="text-[var(--color-cyber-accent)] opacity-70" size={20} />
          </div>
          <div className="text-4xl font-bold text-white relative z-10">{providers.size}</div>
        </div>

        <div className="glass-panel p-6 rounded-xl hover:-translate-y-1 transition-transform relative overflow-hidden group bg-gradient-to-br from-white/5 to-[var(--color-cyber-neon)]/10">
          <div className="flex justify-between items-start mb-4 relative z-10">
            <h3 className="text-gray-400 uppercase tracking-widest text-xs font-semibold">Market Trend</h3>
            <TrendingDown className="text-green-400 opacity-70" size={20} />
          </div>
          <div className="text-4xl font-bold text-white relative z-10">-2.4%</div>
          <p className="text-xs text-green-400 mt-2">Avg price drop (24h)</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Chart Section */}
        <div className="lg:col-span-1 glass-panel p-6 rounded-xl flex flex-col">
          <h2 className="text-lg font-bold text-white mb-6">Market Supply (Top 5)</h2>
          <div className="flex-1 min-h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                <XAxis dataKey="name" stroke="#666" fontSize={10} tickLine={false} axisLine={false} />
                <YAxis stroke="#666" fontSize={10} tickLine={false} axisLine={false} />
                <Tooltip 
                  cursor={{fill: 'rgba(255,255,255,0.05)'}}
                  contentStyle={{ backgroundColor: 'rgba(10,10,15,0.9)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                />
                <Bar dataKey="offers" radius={[4, 4, 0, 0]}>
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={index === 0 ? 'var(--color-cyber-neon)' : 'var(--color-cyber-purple)'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Main Table Area */}
        <div className="lg:col-span-2 glass-panel rounded-xl overflow-hidden flex flex-col">
          <div className="p-6 border-b border-white/5 flex justify-between items-center bg-white/5">
            <h2 className="text-xl font-bold text-white">Live Instance Pricing</h2>
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" size={16} />
              <input 
                type="text" 
                placeholder="Search GPUs..." 
                className="bg-black/40 border border-white/10 rounded-full py-2 pl-10 pr-4 text-sm text-white focus:outline-none focus:border-[var(--color-cyber-neon)] transition-colors w-64"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
          <div className="overflow-x-auto max-h-[500px] overflow-y-auto">
            <table className="w-full text-left border-collapse">
              <thead className="sticky top-0 bg-[#12121a]/95 backdrop-blur z-10">
                <tr className="text-gray-400 text-xs uppercase tracking-widest border-b border-white/10">
                  <th className="p-4 font-semibold">Model</th>
                  <th className="p-4 font-semibold">VRAM</th>
                  <th className="p-4 font-semibold">Best Price</th>
                  <th className="p-4 font-semibold">Top Provider</th>
                  <th className="p-4 font-semibold">Total Offers</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {filteredGpus.sort((a, b) => b.offers.length - a.offers.length).map((gpu) => {
                  const sortedOffers = [...gpu.offers].sort((a, b) => a.price_per_hour - b.price_per_hour);
                  const bestOffer = sortedOffers[0];
                  
                  return (
                    <tr key={gpu.id} className="hover:bg-white/5 transition-colors group">
                      <td className="p-4">
                        <div className="font-semibold text-white group-hover:text-neon transition-colors">{gpu.name}</div>
                      </td>
                      <td className="p-4">
                        <span className="inline-block px-2 py-1 bg-white/10 rounded text-xs text-gray-300">
                          {gpu.vram_gb} GB
                        </span>
                      </td>
                      <td className="p-4">
                        {bestOffer ? (
                          <div className="text-neon font-mono font-medium">
                            ${bestOffer.price_per_hour.toFixed(3)}<span className="text-gray-500 text-xs">/hr</span>
                          </div>
                        ) : (
                          <span className="text-gray-600">-</span>
                        )}
                      </td>
                      <td className="p-4">
                        {bestOffer ? (
                          <span className="capitalize text-gray-300">
                            {bestOffer.provider}
                            {!bestOffer.is_available && <span className="ml-2 text-xs text-red-400">(Unavailable)</span>}
                          </span>
                        ) : (
                          <span className="text-gray-600">-</span>
                        )}
                      </td>
                      <td className="p-4 text-gray-400">
                        {gpu.offers.length}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
