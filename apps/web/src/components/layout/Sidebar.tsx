import { Cpu, Database, HardDrive, Server, Shield, Activity } from "lucide-react";

interface SidebarProps {
  selectedCategory: string;
  setSelectedCategory: (category: string) => void;
}

export default function Sidebar({ selectedCategory, setSelectedCategory }: SidebarProps) {
  const menuItems = [
    { id: "gpu", label: "GPU 인스턴스", icon: <Cpu size={18} /> },
    { id: "cpu", label: "CPU 인스턴스", icon: <Server size={18} /> },
    { id: "memory", label: "메모리 (RAM)", icon: <Database size={18} /> },
    { id: "storage", label: "스토리지 (NVMe)", icon: <HardDrive size={18} /> },
    { id: "baremetal", label: "베어메탈", icon: <Shield size={18} /> },
    { id: "api", label: "API 시세연동", icon: <Activity size={18} /> },
  ];

  return (
    <aside className="w-64 shrink-0 hidden lg:block">
      <div className="bg-white border border-slate-200/60 rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] overflow-hidden sticky top-24">
        <div className="p-5 border-b border-slate-100 bg-slate-50/50">
          <h2 className="font-extrabold text-slate-800 text-sm tracking-wide">카테고리</h2>
        </div>
        <nav className="p-3 flex flex-col gap-1">
          {menuItems.map((item) => {
            const isSelected = selectedCategory === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setSelectedCategory(item.id)}
                className={`flex items-center gap-3 px-4 py-3 rounded-2xl transition-all duration-200 text-sm font-bold ${
                  isSelected 
                    ? "bg-brand-blue text-white shadow-md shadow-brand-blue/20 translate-x-1" 
                    : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                }`}
              >
                <span className={isSelected ? "text-white" : "text-slate-400"}>{item.icon}</span>
                {item.label}
              </button>
            );
          })}
        </nav>
      </div>
    </aside>
  );
}
