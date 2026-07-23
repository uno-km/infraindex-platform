"use client";

import React, { useEffect, useState } from 'react';
import { Newspaper, Search, ExternalLink, Filter, TrendingUp, Clock, Tag } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';
import { ko } from 'date-fns/locale';

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? 'http://127.0.0.1:8000/api/v1';

interface NewsItem {
  id: string;
  title: string;
  url: string;
  source_name: string;
  published_at: string;
  summary: string;
  category: string | null;
  is_semiconductor_related: boolean;
  content_type: string;
}

export default function NewsPage() {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState<string>("All");

  const loadNews = async () => {
    setLoading(true);
    try {
      const qs = new URLSearchParams();
      if (search) qs.append('query', search);
      if (filter !== "All") qs.append('category', filter);
      
      const res = await fetch(`${API_BASE}/news?${qs.toString()}`);
      if (res.ok) {
        const data = await res.json();
        setNews(data.items || []);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const delayDebounce = setTimeout(() => {
      loadNews();
    }, 500);
    return () => clearTimeout(delayDebounce);
  }, [search, filter]);

  return (
    <div className="min-h-screen bg-neutral-950 p-8 text-neutral-100 font-sans">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
          <div className="space-y-2">
            <h1 className="text-4xl font-black tracking-tight bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent flex items-center gap-3">
              <Newspaper className="w-10 h-10 text-emerald-400" />
              Global Tech News
            </h1>
            <p className="text-neutral-400 text-lg">Real-time IT & Semiconductor intelligence feed</p>
          </div>
          
          <div className="relative w-full md:w-96">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
              <Search className="w-5 h-5 text-neutral-500" />
            </div>
            <input
              type="text"
              placeholder="Search intelligence..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-neutral-900/50 border border-neutral-800 focus:border-emerald-500/50 rounded-2xl py-3 pl-12 pr-4 text-neutral-200 placeholder:text-neutral-600 outline-none transition-all duration-300 backdrop-blur-xl hover:bg-neutral-900"
            />
          </div>
        </div>

        {/* Filter Chips */}
        <div className="flex items-center gap-3 overflow-x-auto pb-2 scrollbar-hide">
          <Filter className="w-5 h-5 text-neutral-500 mr-2" />
          {["All", "반도체", "GPU", "메모리", "데이터센터"].map((cat) => (
            <button
              key={cat}
              onClick={() => setFilter(cat)}
              className={`px-5 py-2 rounded-full text-sm font-medium transition-all duration-300 whitespace-nowrap ${
                filter === cat 
                ? 'bg-gradient-to-r from-emerald-500 to-emerald-600 text-white shadow-lg shadow-emerald-500/20' 
                : 'bg-neutral-900 text-neutral-400 hover:bg-neutral-800 hover:text-white border border-neutral-800'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Grid Layout */}
        {loading ? (
          <div className="flex justify-center items-center py-32">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {news.map((item) => (
              <a 
                href={item.url} 
                target="_blank" 
                rel="noreferrer"
                key={item.id}
                className="group relative flex flex-col bg-neutral-900/40 backdrop-blur-sm border border-neutral-800/60 rounded-3xl p-6 hover:bg-neutral-800/60 transition-all duration-500 hover:-translate-y-1 hover:shadow-2xl hover:shadow-emerald-500/10 overflow-hidden"
              >
                {/* Deco line */}
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-500/0 via-emerald-500/0 to-emerald-500/0 group-hover:from-emerald-500/50 group-hover:via-cyan-500/50 group-hover:to-blue-500/50 transition-all duration-500"></div>
                
                <div className="flex justify-between items-start mb-4">
                  <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-neutral-800 text-xs font-medium text-emerald-400">
                    {item.source_name}
                  </span>
                  <div className="flex items-center gap-1.5 text-xs text-neutral-500">
                    <Clock className="w-3.5 h-3.5" />
                    {item.published_at ? formatDistanceToNow(new Date(item.published_at), { addSuffix: true, locale: ko }) : 'Unknown'}
                  </div>
                </div>

                <h3 className="text-xl font-bold text-neutral-100 leading-snug mb-3 group-hover:text-emerald-400 transition-colors line-clamp-3">
                  {item.title}
                </h3>
                
                <p className="text-sm text-neutral-400 line-clamp-3 mb-6 flex-grow leading-relaxed">
                  {item.summary || "No summary available."}
                </p>

                <div className="flex items-center justify-between mt-auto pt-4 border-t border-neutral-800/60">
                  <div className="flex items-center gap-2">
                    {item.category && (
                      <span className="inline-flex items-center gap-1 text-xs text-cyan-400 bg-cyan-400/10 px-2 py-1 rounded-md">
                        <Tag className="w-3 h-3" />
                        {item.category}
                      </span>
                    )}
                    {item.is_semiconductor_related && (
                      <span className="inline-flex items-center gap-1 text-xs text-purple-400 bg-purple-400/10 px-2 py-1 rounded-md">
                        <TrendingUp className="w-3 h-3" />
                        Semiconductor
                      </span>
                    )}
                  </div>
                  <ExternalLink className="w-5 h-5 text-neutral-600 group-hover:text-emerald-400 transition-colors" />
                </div>
              </a>
            ))}
          </div>
        )}

        {!loading && news.length === 0 && (
          <div className="text-center py-32 text-neutral-500">
            <Newspaper className="w-16 h-16 mx-auto mb-4 opacity-20" />
            <p className="text-xl">No intelligence found matching your criteria.</p>
          </div>
        )}
      </div>
    </div>
  );
}
