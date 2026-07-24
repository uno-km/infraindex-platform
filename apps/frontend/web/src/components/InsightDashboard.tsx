"use client";

import React, { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import { Activity, BarChart2, TrendingUp, AlertTriangle, Lightbulb } from "lucide-react";

const Chart = dynamic(() => import("react-apexcharts"), { ssr: false });

export default function InsightDashboard() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [products, setProducts] = useState<any[]>([]);
  const [productId, setProductId] = useState("");
  const [timeframe, setTimeframe] = useState("3M");

  // We want to fetch 3 indicators for the 3 charts
  const indicators = [
    { id: "SOXX", name: "필라델피아 반도체 지수" },
    { id: "NVDA", name: "엔비디아 (NVDA)" },
    { id: "DRAM", name: "DRAM DXI 지수" }
  ];
  
  const [datasets, setDatasets] = useState<any>({});

  // Load products for dropdown
  useEffect(() => {
    fetch(`/api/v1/market/products?limit=20`)
      .then(res => res.json())
      .then(json => {
        setProducts(json);
        if (json.length > 0) setProductId(json[0].id);
      })
      .catch(err => console.error(err));
  }, []);

  // Fetch correlation data for all 3 indicators
  useEffect(() => {
    if (!productId) return;
    
    const fetchCorrelations = async () => {
      setLoading(true);
      setError("");
      
      try {
        const ohlcRes = await fetch(`/api/v1/market/products/${productId}/prices?period=${timeframe}`);
        if (!ohlcRes.ok) throw new Error("Failed to fetch product prices");
        const seriesA = await ohlcRes.json();
        
        const newDatasets: any = {};
        
        // Fetch all indicators in parallel
        await Promise.all(indicators.map(async (ind) => {
          const corrRes = await fetch(`/api/v1/market/correlation`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ series_a: seriesA, indicator_type: ind.id })
          });
          if (corrRes.ok) {
            const data = await corrRes.json();
            if (!data.error) {
              newDatasets[ind.id] = data;
            }
          }
        }));
        
        setDatasets(newDatasets);
      } catch (err: any) {
        console.error("Correlation API failed:", err);
        setError(err.message || "Failed to load correlation data");
        setDatasets({});
      } finally {
        setLoading(false);
      }
    };
    
    fetchCorrelations();
  }, [productId, timeframe]);

  const getChartOptions = (title: string) => ({
    chart: { type: "line", background: "transparent", toolbar: { show: false } },
    theme: { mode: "light" },
    colors: ['#3b82f6', '#10b981'], // Blue for product, Emerald for indicator
    stroke: { curve: 'smooth', width: 2 },
    title: { text: title, align: 'left', style: { color: '#1e293b', fontSize: '14px', fontWeight: 'bold' } },
    xaxis: { type: 'datetime', labels: { style: { colors: "#64748b" } } },
    yaxis: { title: { text: "Norm. Index" }, labels: { style: { colors: "#64748b" } }, decimalsInFloat: 1 },
    tooltip: { shared: true, intersect: false },
    legend: { labels: { colors: "#475569" }, position: 'top' },
    grid: { borderColor: '#f1f5f9' }
  });

  return (
    <div className="bg-white border border-slate-200/60 rounded-3xl p-6 shadow-[0_8px_30px_rgb(0,0,0,0.04)] animate-in fade-in zoom-in duration-700">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 border-b border-slate-100 pb-4 gap-4">
        <div>
          <h2 className="text-2xl font-bold flex items-center gap-3 text-slate-800">
            <Lightbulb className="text-amber-500 w-7 h-7" />
            시장 교차 분석 (다중 상관관계)
          </h2>
          <p className="text-slate-500 text-sm mt-1 font-medium">
            현물 하드웨어 시세와 거시경제 금융 지표 간의 다차원 상관성을 한눈에 분석합니다.
          </p>
        </div>
        
        <div className="flex flex-wrap gap-3 items-center">
          <select 
            className="bg-slate-50 border border-slate-200 text-slate-700 font-semibold text-sm rounded-xl focus:ring-2 focus:ring-indigo-100 focus:border-indigo-500 p-2.5 outline-none cursor-pointer"
            value={productId}
            onChange={(e) => setProductId(e.target.value)}
          >
            {products.length === 0 && <option value="">상품 선택</option>}
            {products.map(p => (
              <option key={p.id} value={p.id}>{p.manufacturer} {p.model_name}</option>
            ))}
          </select>

          <select 
            className="bg-slate-50 border border-slate-200 text-slate-700 font-semibold text-sm rounded-xl focus:ring-2 focus:ring-indigo-100 focus:border-indigo-500 p-2.5 outline-none cursor-pointer"
            value={timeframe}
            onChange={(e) => setTimeframe(e.target.value)}
          >
            <option value="1M">최근 1개월</option>
            <option value="3M">최근 3개월</option>
            <option value="6M">최근 6개월</option>
            <option value="1Y">최근 1년</option>
          </select>
        </div>
      </div>

      {loading && (
        <div className="flex justify-center items-center h-[500px]">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-amber-500"></div>
        </div>
      )}

      {error && (
        <div className="flex justify-center items-center h-[200px] text-red-500 bg-red-50 rounded-2xl border border-red-100 font-bold">
          <AlertTriangle className="w-5 h-5 mr-2" />
          {error}
        </div>
      )}

      {!loading && !error && Object.keys(datasets).length > 0 && (
        <div className="space-y-8">
          
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
            {indicators.map((ind) => {
              const data = datasets[ind.id];
              if (!data) return null;
              
              const series = [
                { name: "가격 흐름", data: data.values_a_normalized },
                { name: ind.name, data: data.values_b_normalized }
              ];

              return (
                <div key={ind.id} className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm hover:shadow-md transition-shadow">
                  <div className="flex justify-between items-end mb-4">
                    <div>
                      <div className="text-slate-400 text-[10px] font-black uppercase tracking-widest mb-1">vs {ind.name}</div>
                      <div className="text-3xl font-black text-slate-800 flex items-baseline gap-1">
                        {data.pearson_correlation}
                        <span className="text-xs text-slate-400 font-medium">상관계수</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-xs text-slate-500 font-bold">Spearman</div>
                      <div className="text-sm font-black text-indigo-600">{data.spearman_correlation}</div>
                    </div>
                  </div>
                  
                  <div className="h-[250px] w-full">
                    <Chart options={getChartOptions(`${ind.name} 벤치마크`) as any} series={series} type="line" height="100%" />
                  </div>
                </div>
              );
            })}
          </div>

          <div className="bg-amber-50 border border-amber-200 rounded-2xl p-5 flex gap-4 text-sm text-amber-800 items-start">
            <AlertTriangle className="w-6 h-6 shrink-0 mt-0.5 text-amber-500" />
            <div>
              <p className="font-bold text-amber-900 mb-1 text-base">지표 분석 주의사항</p>
              <p className="font-medium opacity-90">{datasets[indicators[0].id]?.warning || "분석을 위한 정규화 데이터입니다."}</p>
              <p className="mt-1 opacity-75">
                모든 차트는 기준일자를 100으로 환산하여 가격 규모가 아닌 변동성과 흐름의 상관성만을 교차 검증합니다. 상관계수가 높다고 하여 절대적인 인과관계를 의미하지는 않습니다.
              </p>
            </div>
          </div>

        </div>
      )}
      
      {!loading && !error && Object.keys(datasets).length === 0 && (
         <div className="flex justify-center items-center h-[300px] text-slate-400 font-bold bg-slate-50 rounded-2xl border border-slate-100">
           데이터가 부족하여 상관관계를 분석할 수 없습니다.
         </div>
      )}
    </div>
  );
}
