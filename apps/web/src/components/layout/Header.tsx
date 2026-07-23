"use client";

import { Search, User, Activity, Bookmark, Cloud, Settings, LogOut } from "lucide-react";

import { useAuth } from "../../context/AuthContext";

interface HeaderProps {
  searchQuery: string;
  setSearchQuery: (val: string) => void;
}

export default function Header({ searchQuery, setSearchQuery }: HeaderProps) {
  const { isAuthenticated, logout } = useAuth();

  return (
    <header className="bg-white/90 backdrop-blur-md border-b border-slate-300 sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto flex items-center justify-between py-4 px-6">
        <div className="flex items-center gap-8">
          <div className="text-2xl font-black text-indigo-700 tracking-tight cursor-pointer flex items-center">
            <Cloud className="mr-2" size={28} strokeWidth={2.5} /> InfraIndex
            <span className="text-sm text-slate-600 font-bold ml-4 tracking-normal hidden md:inline-block border-l border-slate-300 pl-4 py-1">글로벌 클라우드 자원 거래소</span>
          </div>
        </div>

        <div className="flex-1 max-w-lg mx-8">
          <div className="relative flex items-center group">
            <input 
              type="text" 
              placeholder="검색할 자원 모델명 입력 (예: H100, RTX 4090)" 
              className="w-full bg-slate-50 border border-slate-300 focus:bg-white focus:border-indigo-600 focus:ring-4 focus:ring-indigo-100 rounded-2xl py-2.5 px-5 text-sm font-medium text-slate-800 placeholder-slate-400 outline-none transition-all duration-300 shadow-inner"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
            />
            <button className="absolute right-4 text-slate-500 group-focus-within:text-indigo-700 transition-colors">
              <Search size={18} strokeWidth={2.5} />
            </button>
          </div>
        </div>

        <div className="flex gap-7 items-center text-slate-700">
          <div className="flex items-center gap-2 cursor-pointer hover:text-indigo-700 transition-colors">
            <Activity size={18} strokeWidth={2.5} />
            <span className="text-sm font-bold hidden sm:block">시장 데이터</span>
          </div>
          <div className="flex items-center gap-2 cursor-pointer hover:text-indigo-700 transition-colors">
            <Bookmark size={18} strokeWidth={2.5} />
            <span className="text-sm font-bold hidden sm:block">관심 자원</span>
          </div>
          
          {isAuthenticated && user ? (
            <div className="flex items-center gap-4">
              <span className="text-sm font-medium text-slate-700 hidden sm:block">
                <span className="font-bold text-indigo-700">{user.nickname}</span>님 안녕하세요
              </span>
              
              {user.is_admin ? (
                <a 
                  href="/admin"
                  className="flex items-center gap-2 cursor-pointer bg-slate-900 hover:bg-indigo-600 text-white px-4 py-2 rounded-xl transition-all shadow-md hover:shadow-indigo-200"
                >
                  <Settings size={16} strokeWidth={2.5} />
                  <span className="text-sm font-bold hidden sm:block">관리하기</span>
                </a>
              ) : (
                <div 
                  className="flex items-center gap-2 cursor-pointer bg-slate-100 hover:bg-slate-200 text-slate-700 px-4 py-2 rounded-xl transition-all shadow-sm"
                >
                  <User size={16} strokeWidth={2.5} />
                  <span className="text-sm font-bold hidden sm:block">마이페이지</span>
                </div>
              )}
              
              <button 
                onClick={logout}
                className="p-2 text-slate-400 hover:text-red-500 transition-colors ml-2"
                title="로그아웃"
              >
                <LogOut size={20} />
              </button>
            </div>
          ) : (
            <div 
              onClick={() => window.dispatchEvent(new CustomEvent('open-login-modal'))}
              className="flex items-center gap-2 cursor-pointer bg-slate-900 hover:bg-indigo-700 text-white px-4 py-2 rounded-xl transition-all shadow-md shadow-slate-300 hover:shadow-indigo-200"
            >
              <User size={16} strokeWidth={2.5} />
              <span className="text-sm font-bold hidden sm:block">로그인</span>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
