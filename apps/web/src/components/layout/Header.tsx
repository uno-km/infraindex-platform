import { Search, Info, Settings } from "lucide-react";
import Link from "next/link";

interface HeaderProps {
  searchQuery: string;
  setSearchQuery: (query: string) => void;
}

export default function Header({ searchQuery, setSearchQuery }: HeaderProps) {
  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-8">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-brand-blue rounded flex items-center justify-center text-white font-bold text-xl">
              I
            </div>
            <span className="font-extrabold text-xl text-slate-800 tracking-tight">Infra<span className="text-brand-blue">Index</span></span>
          </Link>

          <div className="hidden md:flex relative w-96">
            <input 
              type="text" 
              placeholder="GPU, 클라우드 등 모델명 검색" 
              className="w-full bg-slate-100 border border-slate-200 rounded-full py-2 pl-4 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-brand-blue/30 focus:border-brand-blue transition-all font-medium text-slate-700"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <Search className="absolute right-3 top-1/2 -translate-y-1/2 text-brand-blue" size={18} />
          </div>
        </div>

        <div className="flex items-center gap-4">
          <button className="p-2 text-slate-500 hover:bg-slate-100 rounded-full transition-colors">
            <Info size={20} />
          </button>
          <button className="p-2 text-slate-500 hover:bg-slate-100 rounded-full transition-colors">
            <Settings size={20} />
          </button>
        </div>
      </div>
    </header>
  );
}
