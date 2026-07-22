"use client";

import { Menu, ChevronRight, Server, Cpu, HardDrive, Cloud } from "lucide-react";

interface SidebarProps {
  selectedCategory: string;
  setSelectedCategory: (val: string) => void;
}

export default function Sidebar({ selectedCategory, setSelectedCategory }: SidebarProps) {
  const categories = [
    { id: "gpu", icon: <Server size={18}/>, name: "GPU 인스턴스" },
    { id: "cpu", icon: <Cpu size={18}/>, name: "CPU 컴퓨팅" },
    { id: "storage", icon: <HardDrive size={18}/>, name: "스토리지 & 블록" },
    { id: "baremetal", icon: <Cloud size={18}/>, name: "베어메탈 서버" },
  ];

  return (
    <aside className="w-64 flex-shrink-0 bg-white border border-slate-200/60 rounded-3xl overflow-hidden sticky top-[100px] shadow-[0_8px_30px_rgb(0,0,0,0.04)]">
      <div className="bg-white text-slate-800 py-5 px-6 flex items-center font-extrabold text-sm tracking-wide border-b border-slate-100">
        <Menu className="mr-3 text-slate-400" size={18} /> 리소스 카테고리
      </div>
      <ul className="py-2">
        {categories.map((cat) => {
          const active = selectedCategory === cat.id;
          return (
            <li 
              key={cat.id} 
              onClick={() => setSelectedCategory(cat.id)}
              className={`px-6 py-3.5 text-sm font-semibold border-b border-slate-50 last:border-0 cursor-pointer flex justify-between items-center transition-all duration-200 ${active ? 'bg-indigo-50/50 text-indigo-700 border-l-4 border-indigo-600 pl-5' : 'text-slate-500 hover:bg-slate-50 hover:text-indigo-600'}`}
            >
              <span className="flex items-center gap-3">
                <span className={`${active ? 'text-indigo-500' : 'text-slate-400'}`}>{cat.icon}</span>
                {cat.name}
              </span>
              {active && <ChevronRight size={16} className="text-indigo-400" />}
            </li>
          );
        })}
      </ul>
    </aside>
  );
}
