"use client";

import React, { useEffect, useState } from "react";

export default function NewsDashboard() {
  const [news, setNews] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/v1/news?limit=30")
      .then((res) => {
        if (!res.ok) throw new Error("API_ERROR");
        return res.json();
      })
      .then((data) => {
        if (Array.isArray(data)) {
          setNews(data);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error("News API failed:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-gray-500">
        Loading global news...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-teal-400">
            Global Market News
          </h2>
          <p className="text-gray-400 text-sm mt-1">
            Real-time semiconductor & IT insights from around the world
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {news.map((item) => (
          <a
            key={item.id}
            href={item.url}
            target="_blank"
            rel="noopener noreferrer"
            className="block p-5 bg-gray-900 border border-gray-800 rounded-xl hover:border-blue-500 transition-colors shadow-lg hover:shadow-blue-500/20"
          >
            <div className="flex justify-between items-start mb-3">
              <span className="text-xs font-semibold px-2 py-1 rounded bg-blue-500/20 text-blue-400">
                {item.source}
              </span>
              <span className="text-xs text-gray-500">
                {new Date(item.published_at).toLocaleDateString()}
              </span>
            </div>
            
            <h3 className="text-lg font-semibold text-white mb-2 line-clamp-2">
              {item.title}
            </h3>
            
            {item.summary && (
              <p className="text-sm text-gray-400 line-clamp-3 mb-4">
                {item.summary}
              </p>
            )}

            <div className="flex flex-wrap gap-1 mt-auto">
              {item.keywords?.split(",").map((kw: string) => (
                <span key={kw} className="text-[10px] text-gray-400 bg-gray-800 px-2 py-0.5 rounded">
                  #{kw.trim()}
                </span>
              ))}
            </div>
          </a>
        ))}

        {news.length === 0 && (
          <div className="col-span-full text-center text-gray-500 py-12 bg-gray-900 border border-gray-800 rounded-xl">
            No news articles found in the database.
          </div>
        )}
      </div>
    </div>
  );
}
