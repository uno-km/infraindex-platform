"use client";

import { Menu, ChevronRight, Server, Cpu, HardDrive, Cloud, BarChart2, Building, Lightbulb, Newspaper, TrendingUp } from "lucide-react";

interface SidebarProps {
  selectedCategory: string;
  setSelectedCategory: (val: string) => void;
}

export default function Sidebar({ selectedCategory, setSelectedCategory }: SidebarProps) {
  const sections = [
    {
      title: "리소스 카테고리",
      icon: <Menu className="mr-3 text-slate-400" size={18} />,
      items: [
        { id: "gpu", icon: <Server size={18}/>, name: "GPU 인스턴스" },
        { id: "cpu", icon: <Cpu size={18}/>, name: "CPU 컴퓨팅" },
        { id: "storage", icon: <HardDrive size={18}/>, name: "스토리지 & 블록" },
        { id: "baremetal", icon: <Cloud size={18}/>, name: "베어메탈 서버" },
      ]
    },
    {
      title: "시장 분석",
      icon: <TrendingUp className="mr-3 text-slate-400" size={18} />,
      items: [
        { id: "retail", icon: <BarChart2 size={18}/>, name: "리테일 시장" },
        { id: "enterprise", icon: <Building size={18}/>, name: "엔터프라이즈 AI" },
      ]
    },
    {
      title: "인사이트",
      icon: <Lightbulb className="mr-3 text-slate-400" size={18} />,
      items: [
        { id: "insights", icon: <Lightbulb size={18}/>, name: "시장 인사이트" },
        { id: "news", icon: <Newspaper size={18}/>, name: "글로벌 뉴스" },
      ]
    }
  ];

  return (
    <aside className="w-64 flex-shrink-0 bg-white border border-slate-200/60 rounded-3xl overflow-hidden sticky top-[100px] shadow-[0_8px_30px_rgb(0,0,0,0.04)] pb-4">
      {sections.map((section, idx) => (
        <div key={idx} className={idx > 0 ? "mt-4" : ""}>
          <div className="text-slate-800 py-4 px-6 flex items-center font-extrabold text-sm tracking-wide">
            {section.icon} {section.title}
          </div>
          <ul className="py-1">
            {section.items.map((cat) => {
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
        </div>
      ))}
    </aside>
  );
}
