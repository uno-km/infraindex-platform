import { ExternalLink, Zap, Flame } from "lucide-react";

interface Offer {
  provider: string;
  price_per_hour: number;
  is_available: boolean;
  region: string;
  provider_link?: string;
}

interface ResourceItem {
  id: string;
  name: string;
  vram_gb: number;
  popularity_score?: number;
  offers: Offer[];
}

interface ResourceCardProps {
  item: ResourceItem;
  exchangeMultiplier: number;
  currencySymbol: string;
  formatPrice: (price: number) => string;
}

export default function ResourceCard({ item, formatPrice }: ResourceCardProps) {
  // Sort offers by price ascending
  const sortedOffers = [...item.offers].sort((a, b) => a.price_per_hour - b.price_per_hour);
  const bestOffer = sortedOffers[0];
  const isHot = (item.popularity_score || 0) > 80;

  return (
    <div className="p-6 hover:bg-slate-50 transition-colors flex items-center justify-between group">
      {/* Left Info */}
      <div className="flex-1">
        <div className="flex items-center gap-3 mb-2">
          <h4 className="text-xl font-extrabold text-slate-900 group-hover:text-brand-blue transition-colors cursor-pointer">{item.name}</h4>
          {isHot && (
            <span className="bg-rose-100 text-rose-600 px-2 py-0.5 rounded text-xs font-bold flex items-center gap-1">
              <Flame size={12} className="fill-rose-600" /> HOT
            </span>
          )}
        </div>
        <div className="flex items-center gap-4 text-sm text-slate-500 font-medium">
          <div className="flex items-center gap-1.5 bg-slate-100 px-2 py-1 rounded">
            <Zap size={14} className="text-amber-500" /> VRAM <span className="font-bold text-slate-700">{item.vram_gb} GB</span>
          </div>
          <div>판매처 <span className="font-bold text-slate-700">{item.offers.length}</span>곳</div>
        </div>
      </div>

      {/* Right Pricing & Action */}
      <div className="flex items-center gap-8 shrink-0">
        <div className="text-right">
          <div className="text-xs text-slate-400 font-semibold mb-1">최저가 ({bestOffer?.provider})</div>
          {bestOffer ? (
            <div className="text-2xl font-extrabold text-brand-red tracking-tight">
              {formatPrice(bestOffer.price_per_hour)}<span className="text-sm text-slate-500 font-medium tracking-normal"> / 시간</span>
            </div>
          ) : (
            <div className="text-slate-400 font-medium">재고 없음</div>
          )}
        </div>

        <a 
          href={bestOffer?.provider_link || "#"} 
          target="_blank" 
          rel="noopener noreferrer"
          className={`flex items-center gap-2 px-6 py-3 rounded-xl font-bold text-sm transition-all ${
            bestOffer 
              ? "bg-brand-red text-white hover:bg-rose-700 shadow-lg shadow-rose-200" 
              : "bg-slate-200 text-slate-400 cursor-not-allowed"
          }`}
        >
          렌탈하러 가기
          <ExternalLink size={16} />
        </a>
      </div>
    </div>
  );
}
