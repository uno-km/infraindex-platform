"use client";

import React, { useEffect, useState, useCallback } from "react";
import { Search, Video, Newspaper, Filter, ExternalLink, PlayCircle } from "lucide-react";
import Image from "next/image";

export default function NewsDashboard() {
  const [news, setNews] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  
  // Filters
  const [query, setQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");
  const [category, setCategory] = useState<string>("");
  const [contentType, setContentType] = useState<string>("");
  const [isSemiconductor, setIsSemiconductor] = useState<boolean>(false);
  
  const categories = ["", "GPU", "반도체", "메모리", "데이터센터"];

  // Debounce search query
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedQuery(query), 500);
    return () => clearTimeout(timer);
  }, [query]);

  const fetchNews = useCallback(async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      params.append("limit", "50");
      if (debouncedQuery) params.append("query", debouncedQuery);
      if (category) params.append("category", category);
      if (contentType) params.append("content_type", contentType);
      if (isSemiconductor) params.append("is_semiconductor_related", "true");

      const res = await fetch(`/api/v1/news?${params.toString()}`);
      if (!res.ok) throw new Error("API_ERROR");
      const data = await res.json();
      setNews(Array.isArray(data) ? data : (data?.items || []));
    } catch (err) {
      console.error("News API failed:", err);
      setNews([]);
    } finally {
      setLoading(false);
    }
  }, [debouncedQuery, category, contentType, isSemiconductor]);

  useEffect(() => {
    fetchNews();
  }, [fetchNews]);

  const getTimeAgo = (dateStr: string) => {
    if (!dateStr) return "";
    const diff = Date.now() - new Date(dateStr).getTime();
    const hours = Math.floor(diff / (1000 * 60 * 60));
    if (hours < 1) return "방금 전";
    if (hours < 24) return `${hours}시간 전`;
    return `${Math.floor(hours / 24)}일 전`;
  };

  return (
    <div className="w-full max-w-5xl mx-auto space-y-6">
      {/* Header & Controls */}
      <div className="bg-white rounded-2xl shadow-sm border border-slate-200/60 p-5 md:p-6 mb-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          <div>
            <h2 className="text-2xl font-bold text-slate-800 flex items-center gap-2">
              <span className="bg-gradient-to-r from-indigo-600 to-indigo-400 text-transparent bg-clip-text">
                글로벌 IT 리서치 피드
              </span>
            </h2>
            <p className="text-slate-500 text-sm mt-1">
              반도체, 메모리, 데이터센터, AI 최신 동향
            </p>
          </div>
          
          {/* Search */}
          <div className="relative w-full md:w-72">
            <input 
              type="text" 
              placeholder="검색어를 입력하세요..." 
              className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-indigo-100 focus:border-indigo-500 outline-none transition-all"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-4 h-4" />
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-col md:flex-row gap-4 items-start md:items-center justify-between border-t border-slate-100 pt-4">
          <div className="flex flex-wrap gap-2">
            {categories.map(cat => (
              <button
                key={cat}
                onClick={() => setCategory(cat)}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${
                  category === cat 
                    ? 'bg-indigo-600 text-white' 
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {cat === "" ? "전체 카테고리" : cat}
              </button>
            ))}
          </div>
          
          <div className="flex items-center gap-2">
            <button
              onClick={() => setIsSemiconductor(!isSemiconductor)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium border transition-colors flex items-center gap-1 ${
                isSemiconductor 
                  ? 'bg-emerald-50 border-emerald-200 text-emerald-700' 
                  : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
              }`}
            >
              <Filter className="w-4 h-4" />
              반도체 관련만
            </button>

            <select 
              className="px-3 py-1.5 rounded-lg text-sm font-medium bg-white border border-slate-200 text-slate-600 outline-none cursor-pointer"
              value={contentType}
              onChange={(e) => setContentType(e.target.value)}
            >
              <option value="">모든 콘텐츠</option>
              <option value="article">기사만</option>
              <option value="youtube">유튜브만</option>
            </select>
          </div>
        </div>
      </div>

      {/* Feed */}
      <div className="space-y-4">
        {loading ? (
          <div className="flex justify-center items-center py-20">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600"></div>
          </div>
        ) : news.length === 0 ? (
          <div className="text-center py-20 bg-white rounded-2xl border border-slate-200/60 shadow-sm text-slate-500">
            검색 조건에 맞는 콘텐츠가 없습니다.
          </div>
        ) : (
          news.map((item) => (
            <a 
              key={item.id} 
              href={item.url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="flex flex-col sm:flex-row bg-white rounded-2xl border border-slate-200/60 p-4 shadow-sm hover:shadow-md hover:border-indigo-200 transition-all group overflow-hidden gap-5"
            >
              {/* Thumbnail Area */}
              {item.thumbnail_url && (
                <div className="relative w-full sm:w-48 h-32 sm:h-auto rounded-xl overflow-hidden shrink-0 bg-slate-100 flex items-center justify-center">
                  {/* We use standard img to easily handle external unknown domains without next/image domains config issues */}
                  <img 
                    src={item.thumbnail_url} 
                    alt={item.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    onError={(e) => { e.currentTarget.style.display = 'none'; }}
                  />
                  {item.content_type === "youtube" && (
                    <div className="absolute inset-0 bg-black/20 flex items-center justify-center group-hover:bg-black/10 transition-colors">
                      <PlayCircle className="w-10 h-10 text-white opacity-90" />
                    </div>
                  )}
                </div>
              )}
              
              {/* Content Area */}
              <div className="flex-1 flex flex-col justify-between">
                <div>
                  <div className="flex flex-wrap items-center gap-2 mb-2">
                    <span className="flex items-center gap-1 text-xs font-semibold px-2 py-1 rounded bg-slate-100 text-slate-600">
                      {item.content_type === 'youtube' ? <Video className="w-3 h-3 text-red-500"/> : <Newspaper className="w-3 h-3"/>}
                      {item.source}
                    </span>
                    {item.category && (
                      <span className="text-xs font-medium px-2 py-1 rounded bg-indigo-50 text-indigo-600 border border-indigo-100">
                        {item.category}
                      </span>
                    )}
                    {item.is_semiconductor_related && (
                      <span className="text-xs font-medium px-2 py-1 rounded bg-emerald-50 text-emerald-600 border border-emerald-100">
                        반도체
                      </span>
                    )}
                    <span className="text-xs text-slate-400 ml-auto" title={new Date(item.published_at).toLocaleString()}>
                      {getTimeAgo(item.published_at)}
                    </span>
                  </div>
                  
                  <h3 className="text-lg font-bold text-slate-800 leading-tight mb-2 group-hover:text-indigo-600 transition-colors">
                    {item.title}
                  </h3>
                  
                  <p className="text-sm text-slate-500 line-clamp-2 leading-relaxed mb-3">
                    {item.summary}
                  </p>
                </div>
                
                <div className="flex items-center justify-between mt-auto">
                  <div className="flex gap-1 flex-wrap">
                    {item.matched_keywords && item.matched_keywords.split(',').filter(Boolean).map((kw: string) => (
                      <span key={kw} className="text-[10px] text-slate-400 bg-slate-50 border border-slate-100 px-1.5 py-0.5 rounded">
                        #{kw.trim()}
                      </span>
                    ))}
                  </div>
                  <span className="text-xs text-indigo-500 font-medium flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                    원문 보기 <ExternalLink className="w-3 h-3" />
                  </span>
                </div>
              </div>
            </a>
          ))
        )}
      </div>
    </div>
  );
}
