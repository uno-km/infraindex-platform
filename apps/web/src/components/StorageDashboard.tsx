"use client";

/**
 * StorageDashboard.tsx
 * 전세계 클라우드 스토리지 대여 가격 대시보드
 * 
 * - AWS, GCP, Azure, Cloudflare R2, Backblaze, Wasabi, 국내(네이버/KT/카카오) 등
 * - POST /api/v1/chart/storage/sync-global 로 데이터 동기화
 * - GET /api/v1/chart/unified?hw_typ=storage 로 차트 데이터 조회
 */

import React, { useState, useEffect, useCallback } from "react";
import {
  HardDrive,
  RefreshCw,
  ExternalLink,
  Database,
  Globe,
  TrendingDown,
  AlertCircle,
} from "lucide-react";
import dynamic from "next/dynamic";

const Chart = dynamic(() => import("react-apexcharts"), { ssr: false });

// 전세계 스토리지 공급자 공개 가격표 (프론트에서도 표시용)
const STORAGE_CATALOG = [
  // 대형 클라우드
  { provider: "AWS", product: "EBS gp3", type: "Block SSD", price_usd: 0.08, region: "us-east-1", tier: "Standard", url: "https://aws.amazon.com/ebs/pricing/" },
  { provider: "AWS", product: "EBS io2", type: "Block SSD", price_usd: 0.125, region: "us-east-1", tier: "Premium", url: "https://aws.amazon.com/ebs/pricing/" },
  { provider: "AWS", product: "S3 Standard", type: "Object", price_usd: 0.023, region: "us-east-1", tier: "Standard", url: "https://aws.amazon.com/s3/pricing/" },
  { provider: "Google Cloud", product: "Persistent Disk SSD", type: "Block SSD", price_usd: 0.17, region: "us-central1", tier: "Standard", url: "https://cloud.google.com/compute/disks-image-pricing" },
  { provider: "Google Cloud", product: "Cloud Storage Standard", type: "Object", price_usd: 0.020, region: "us-central1", tier: "Standard", url: "https://cloud.google.com/storage/pricing" },
  { provider: "Microsoft Azure", product: "Managed Disk Premium SSD", type: "Block SSD", price_usd: 0.135, region: "eastus", tier: "Premium", url: "https://azure.microsoft.com/en-us/pricing/details/managed-disks/" },
  { provider: "Microsoft Azure", product: "Blob Storage Hot", type: "Object", price_usd: 0.018, region: "eastus", tier: "Hot", url: "https://azure.microsoft.com/en-us/pricing/details/storage/blobs/" },
  // 저가 오브젝트 스토리지
  { provider: "Cloudflare R2", product: "R2 Object Storage", type: "Object", price_usd: 0.015, region: "Global", tier: "Standard", url: "https://developers.cloudflare.com/r2/pricing/" },
  { provider: "Backblaze", product: "B2 Cloud Storage", type: "Object", price_usd: 0.006, region: "US-West", tier: "Standard", url: "https://www.backblaze.com/b2/cloud-storage-pricing.html" },
  { provider: "Wasabi", product: "Wasabi Hot Cloud", type: "Object", price_usd: 0.0068, region: "us-east-1", tier: "Standard", url: "https://wasabi.com/cloud-storage-pricing/" },
  // 중소형
  { provider: "DigitalOcean", product: "Block Storage NVMe", type: "Block SSD", price_usd: 0.10, region: "nyc1", tier: "Standard", url: "https://www.digitalocean.com/pricing/volumes" },
  { provider: "DigitalOcean", product: "Spaces Object Storage", type: "Object", price_usd: 0.02, region: "nyc3", tier: "Standard", url: "https://www.digitalocean.com/pricing/spaces" },
  { provider: "Vultr", product: "Block Storage NVMe", type: "Block SSD", price_usd: 0.08, region: "New Jersey", tier: "NVMe", url: "https://www.vultr.com/products/block-storage/" },
  { provider: "Hetzner", product: "Storage Box HB 10TB", type: "HDD", price_usd: 0.0033, region: "EU", tier: "Economy", url: "https://www.hetzner.com/storage/storage-box" },
  { provider: "Hetzner", product: "Volume Block SSD", type: "Block SSD", price_usd: 0.052, region: "EU", tier: "Standard", url: "https://www.hetzner.com/cloud" },
  { provider: "Linode (Akamai)", product: "Block Storage", type: "Block SSD", price_usd: 0.10, region: "us-east", tier: "Standard", url: "https://www.linode.com/pricing/#storage" },
  { provider: "OVH Cloud", product: "Object Storage Swift", type: "Object", price_usd: 0.011, region: "EU", tier: "Standard", url: "https://www.ovhcloud.com/en/public-cloud/object-storage/" },
  // 국내
  { provider: "NCloud (Naver)", product: "Object Storage", type: "Object", price_usd: null, price_krw: 25, region: "Korea", tier: "Standard", url: "https://www.ncloud.com/product/storage/objectStorage" },
  { provider: "KT Cloud", product: "Object Storage", type: "Object", price_usd: null, price_krw: 22, region: "Korea", tier: "Standard", url: "https://cloud.kt.com" },
  { provider: "Kakao Cloud", product: "Object Storage", type: "Object", price_usd: null, price_krw: 20, region: "Korea", tier: "Standard", url: "https://kakaocloud.com/service/storage" },
];

const TYPE_COLORS: Record<string, string> = {
  "Block SSD": "bg-indigo-50 text-indigo-700 border-indigo-200",
  "Object": "bg-emerald-50 text-emerald-700 border-emerald-200",
  "HDD": "bg-amber-50 text-amber-700 border-amber-200",
};

const TIER_BADGE: Record<string, string> = {
  "Premium": "bg-purple-50 text-purple-700 border-purple-200",
  "NVMe": "bg-blue-50 text-blue-700 border-blue-200",
  "Economy": "bg-gray-50 text-gray-600 border-gray-200",
  "Hot": "bg-orange-50 text-orange-700 border-orange-200",
  "Standard": "bg-slate-50 text-slate-600 border-slate-200",
};

type StorageFilterType = "전체" | "Block SSD" | "Object" | "HDD";

export default function StorageDashboard() {
  const [syncing, setSyncing] = useState(false);
  const [syncResult, setSyncResult] = useState<string | null>(null);
  const [filterType, setFilterType] = useState<StorageFilterType>("전체");
  const [sortBy, setSortBy] = useState<"price_asc" | "provider">("price_asc");
  const [currency, setCurrency] = useState<"USD" | "KRW">("USD");
  const [krwRate, setKrwRate] = useState(1380);
  const [chartSeries, setChartSeries] = useState<any[]>([]);
  const [chartLoading, setChartLoading] = useState(false);

  // 환율 조회
  useEffect(() => {
    fetch("https://open.er-api.com/v6/latest/USD")
      .then(r => r.json())
      .then(d => { if (d?.rates?.KRW) setKrwRate(d.rates.KRW); })
      .catch(() => {});
  }, []);

  // 차트 데이터 조회
  const fetchChartData = useCallback(async () => {
    setChartLoading(true);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/api/v1/chart/unified?hw_typ=storage&days=30`);
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          const series = data.slice(0, 6).map((s: any) => ({
            name: `${s.provider} - ${s.model_name}`,
            data: (s.data || []).map((pt: any) => ({
              x: new Date(pt.time).getTime(),
              y: pt.value,
            })),
          }));
          setChartSeries(series);
        }
      }
    } catch (e) {
      console.error("Chart fetch failed:", e);
    } finally {
      setChartLoading(false);
    }
  }, []);

  useEffect(() => { fetchChartData(); }, [fetchChartData]);

  // 전세계 스토리지 가격 동기화
  const handleSync = async () => {
    setSyncing(true);
    setSyncResult(null);
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${apiUrl}/api/v1/chart/storage/sync-global`, {
        method: "POST",
      });
      const data = await res.json();
      setSyncResult(
        data.status === "success"
          ? `✅ ${data.inserted}개 가격 저장 완료 (${data.providers}개 공급자)`
          : `❌ 오류: ${data.message}`
      );
      if (data.status === "success") fetchChartData();
    } catch (e) {
      setSyncResult("❌ 서버 연결 실패");
    } finally {
      setSyncing(false);
    }
  };

  // 필터 + 정렬 적용
  const displayItems = STORAGE_CATALOG
    .filter(item => filterType === "전체" || item.type === filterType)
    .map(item => ({
      ...item,
      display_price: currency === "USD"
        ? (item.price_usd !== null && item.price_usd !== undefined ? item.price_usd : (item as any).price_krw / krwRate)
        : (item.price_usd !== null && item.price_usd !== undefined ? item.price_usd * krwRate : (item as any).price_krw),
    }))
    .sort((a, b) => {
      if (sortBy === "price_asc") return a.display_price - b.display_price;
      return a.provider.localeCompare(b.provider);
    });

  const lowestItem = displayItems[0];

  const chartOptions: ApexCharts.ApexOptions = {
    chart: { type: "line", height: 280, toolbar: { show: false }, background: "transparent" },
    stroke: { curve: "smooth", width: 2 },
    xaxis: { type: "datetime", labels: { style: { colors: "#94a3b8", fontSize: "11px" } } },
    yaxis: {
      labels: {
        formatter: (v: number) => currency === "KRW" ? `₩${v.toFixed(0)}` : `$${v.toFixed(4)}`,
        style: { colors: "#94a3b8" },
      },
    },
    tooltip: { x: { format: "MM/dd" } },
    legend: { position: "top", fontSize: "11px" },
    grid: { borderColor: "#f1f5f9" },
    colors: ["#6366f1", "#10b981", "#f59e0b", "#3b82f6", "#ef4444", "#8b5cf6"],
  };

  return (
    <div className="space-y-6 animate-in fade-in zoom-in duration-500">
      {/* Header */}
      <div className="bg-white border border-slate-200/60 rounded-2xl p-5 shadow-sm flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 className="text-xl font-extrabold text-slate-900 flex items-center gap-2">
            <Globe className="text-indigo-500 w-6 h-6" />
            글로벌 STORAGE 인스턴스 시세표
          </h2>
          <p className="text-sm text-slate-500 mt-1">
            전세계 {STORAGE_CATALOG.length}개 공급자 · GB/월 기준 · 실시간 환율 적용
          </p>
        </div>
        <div className="flex items-center gap-3">
          {/* 통화 전환 */}
          <div className="flex bg-slate-100 p-1 rounded-xl">
            <button onClick={() => setCurrency("USD")} className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-all ${currency === "USD" ? "bg-white shadow text-slate-900" : "text-slate-500"}`}>$ USD</button>
            <button onClick={() => setCurrency("KRW")} className={`px-3 py-1.5 text-xs font-bold rounded-lg transition-all ${currency === "KRW" ? "bg-white shadow text-slate-900" : "text-slate-500"}`}>₩ KRW</button>
          </div>
          {/* 동기화 버튼 */}
          <button
            onClick={handleSync}
            disabled={syncing}
            className="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-bold rounded-xl transition-all disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${syncing ? "animate-spin" : ""}`} />
            {syncing ? "동기화 중..." : "가격 동기화"}
          </button>
        </div>
      </div>

      {/* 동기화 결과 */}
      {syncResult && (
        <div className={`px-4 py-3 rounded-xl text-sm font-semibold border ${syncResult.startsWith("✅") ? "bg-emerald-50 border-emerald-200 text-emerald-800" : "bg-rose-50 border-rose-200 text-rose-800"}`}>
          {syncResult}
        </div>
      )}

      {/* 최저가 배너 */}
      {lowestItem && (
        <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl p-5 text-white flex items-center justify-between shadow-lg">
          <div>
            <p className="text-indigo-100 text-xs font-bold uppercase tracking-wider mb-1">🏆 현재 최저가</p>
            <p className="text-2xl font-extrabold">
              {currency === "USD"
                ? `$${lowestItem.price_usd?.toFixed(4) ?? "—"} / GB / 월`
                : `₩${lowestItem.display_price.toFixed(2)} / GB / 월`}
            </p>
            <p className="text-indigo-100 text-sm mt-1">{lowestItem.provider} — {lowestItem.product}</p>
          </div>
          <TrendingDown className="w-12 h-12 text-white/40" />
        </div>
      )}

      {/* 필터 */}
      <div className="bg-white border border-slate-200/60 rounded-2xl p-4 shadow-sm flex flex-wrap gap-3 items-center justify-between">
        <div className="flex gap-2">
          {(["전체", "Block SSD", "Object", "HDD"] as StorageFilterType[]).map(t => (
            <button
              key={t}
              onClick={() => setFilterType(t)}
              className={`px-4 py-2 text-xs font-bold rounded-xl border transition-all ${filterType === t ? "bg-indigo-600 text-white border-indigo-600" : "bg-white text-slate-600 border-slate-200 hover:border-indigo-300"}`}
            >
              {t}
            </button>
          ))}
        </div>
        <select
          value={sortBy}
          onChange={e => setSortBy(e.target.value as any)}
          className="text-sm border border-slate-200 rounded-xl px-3 py-2 text-slate-700 font-semibold bg-white outline-none"
        >
          <option value="price_asc">💰 최저가 순</option>
          <option value="provider">🔤 공급자 순</option>
        </select>
      </div>

      {/* 가격 카드 그리드 */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {displayItems.map((item, idx) => (
          <div
            key={idx}
            className={`bg-white border rounded-2xl p-5 shadow-sm hover:shadow-md transition-all hover:-translate-y-0.5 ${idx === 0 ? "border-indigo-300 ring-1 ring-indigo-100" : "border-slate-200/60"}`}
          >
            <div className="flex justify-between items-start mb-3">
              <div>
                <p className="text-xs font-bold text-slate-400 uppercase tracking-wider">{item.provider}</p>
                <p className="text-base font-extrabold text-slate-900 mt-0.5">{item.product}</p>
                <p className="text-xs text-slate-400 mt-0.5">{item.region}</p>
              </div>
              {idx === 0 && (
                <span className="text-xs font-bold bg-indigo-600 text-white px-2 py-1 rounded-lg">최저가</span>
              )}
            </div>

            <div className="flex gap-2 mb-3">
              <span className={`text-xs font-bold px-2 py-1 rounded-lg border ${TYPE_COLORS[item.type] || "bg-slate-50 text-slate-600 border-slate-200"}`}>
                {item.type}
              </span>
              <span className={`text-xs font-bold px-2 py-1 rounded-lg border ${TIER_BADGE[item.tier] || TIER_BADGE["Standard"]}`}>
                {item.tier}
              </span>
            </div>

            <div className="border-t border-slate-100 pt-3 flex justify-between items-center">
              <div>
                <p className="text-xl font-extrabold text-slate-900">
                  {currency === "USD"
                    ? (item.price_usd !== null && item.price_usd !== undefined ? `$${item.price_usd}` : `₩${(item as any).price_krw}`)
                    : (item.price_usd !== null && item.price_usd !== undefined
                        ? `₩${(item.price_usd * krwRate).toFixed(2)}`
                        : `₩${(item as any).price_krw}`)}
                </p>
                <p className="text-xs text-slate-400 font-medium">/ GB / 월</p>
              </div>
              <a
                href={item.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-1 text-xs text-indigo-600 font-bold hover:text-indigo-800 border border-indigo-200 px-3 py-2 rounded-xl hover:bg-indigo-50 transition-all"
              >
                바로가기 <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>
        ))}
      </div>

      {/* 가격 추이 차트 */}
      <div className="bg-white border border-slate-200/60 rounded-2xl p-6 shadow-sm">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-base font-extrabold text-slate-900 flex items-center gap-2">
            <Database className="w-5 h-5 text-indigo-500" />
            스토리지 가격 변동 추이 (₩/GB/월)
          </h3>
          <button
            onClick={fetchChartData}
            className="flex items-center gap-1 text-xs text-slate-500 hover:text-indigo-600 font-semibold border border-slate-200 px-3 py-1.5 rounded-xl transition-all"
          >
            <RefreshCw className={`w-3 h-3 ${chartLoading ? "animate-spin" : ""}`} />
            새로고침
          </button>
        </div>

        {chartSeries.length > 0 ? (
          <Chart
            type="line"
            height={280}
            series={chartSeries}
            options={chartOptions}
          />
        ) : (
          <div className="h-48 flex flex-col items-center justify-center text-slate-400">
            <AlertCircle className="w-10 h-10 mb-3 text-slate-300" />
            <p className="text-sm font-semibold text-slate-500">
              차트 데이터가 없습니다
            </p>
            <p className="text-xs text-slate-400 mt-1 text-center">
              위의 <strong className="text-indigo-600">가격 동기화</strong> 버튼을 눌러<br />
              전세계 스토리지 가격을 수집하세요
            </p>
            <button
              onClick={handleSync}
              disabled={syncing}
              className="mt-4 px-5 py-2 bg-indigo-600 text-white text-sm font-bold rounded-xl hover:bg-indigo-700 transition-all disabled:opacity-50"
            >
              {syncing ? "동기화 중..." : "지금 동기화하기"}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
