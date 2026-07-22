"use client";

import { Search, User, Activity, Bookmark, Cloud } from "lucide-react";

interface HeaderProps {
  searchQuery: string;
  setSearchQuery: (val: string) => void;
}

export default function Header({ searchQuery, setSearchQuery }: HeaderProps) {
  return (
    <header className="bg-white/80 backdrop-blur-md border-b border-slate-200/80 sticky top-0 z-50 shadow-[0_4px_30px_rgb(0,0,0,0.03)]">
      <div className="max-w-7xl mx-auto flex items-center justify-between py-4 px-6">
        <div className="flex items-center gap-8">
          <div className="text-2xl font-black text-indigo-600 tracking-tight cursor-pointer flex items-center">
            <Cloud className="mr-2" size={28} strokeWidth={2.5} /> InfraIndex
            <span className="text-xs text-slate-400 font-medium ml-4 tracking-normal hidden md:inline-block border-l border-slate-200 pl-4 py-1">글로벌 클라우드 자원 거래소</span>
          </div>
        </div>

        <div className="flex-1 max-w-lg mx-8">
          <div className="relative flex items-center group">
            <input 
              type="text" 
              placeholder="검색할 자원 모델명 입력 (예: H100, RTX 4090)" 
              className="w-full bg-slate-100/50 border border-slate-200 focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-50 rounded-2xl py-2.5 px-5 text-sm outline-none transition-all duration-300"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
            />
            <button className="absolute right-4 text-slate-400 group-focus-within:text-indigo-600 transition-colors">
              <Search size={18} />
            </button>
          </div>
        </div>

        <div className="flex gap-7 items-center text-slate-500">
          <div className="flex items-center gap-2 cursor-pointer hover:text-indigo-600 transition-colors">
            <Activity size={18} />
            <span className="text-sm font-semibold hidden sm:block">시장 데이터</span>
          </div>
          <div className="flex items-center gap-2 cursor-pointer hover:text-indigo-600 transition-colors">
            <Bookmark size={18} />
            <span className="text-sm font-semibold hidden sm:block">관심 자원</span>
          </div>
          <div className="flex items-center gap-2 cursor-pointer bg-slate-900 hover:bg-indigo-600 text-white px-4 py-2 rounded-xl transition-all shadow-md shadow-slate-200 hover:shadow-indigo-200">
            <User size={16} />
            <span className="text-sm font-semibold hidden sm:block">로그인</span>
          </div>
        </div>
      </div>
    </header>
  );
}
