import React, { ReactNode } from 'react';
import { Activity } from 'lucide-react';

export interface BaseChartProps {
  title: string;
  icon?: ReactNode;
  description?: string;
  loading?: boolean;
  empty?: boolean;
  emptyMessage?: string;
  children: ReactNode; // 실제 차트 컴포넌트가 들어갈 자리 (추상화된 본체)
  rightHeaderElement?: ReactNode; // 우측 상단 드롭다운이나 필터 등
}

/**
 * BaseChartLayout
 * 차트의 뼈대(Skeleton), 테두리, 제목, 설명, 로딩 상태, 빈 상태 등을 모두 관리하는 공통 부모 객체입니다.
 * 객체지향의 "추상 클래스" 역할을 담당하며, 이 뼈대 안에 Recharts, ApexCharts 등 어떤 차트든 끼워넣을 수 있습니다.
 */
export default function BaseChartLayout({
  title,
  icon = <Activity className="text-emerald-500" size={20} />,
  description,
  loading = false,
  empty = false,
  emptyMessage = "데이터가 없습니다.",
  children,
  rightHeaderElement
}: BaseChartProps) {
  return (
    <div className="bg-white border border-slate-200/60 rounded-3xl p-6 shadow-[0_8px_30px_rgb(0,0,0,0.04)] h-full flex flex-col">
      {/* Header Section */}
      <div className="flex justify-between items-start mb-2">
        <div>
          <h3 className="text-lg font-black text-slate-800 flex items-center gap-2">
            {icon}
            {title}
          </h3>
          {description && (
            <p className="text-sm text-slate-500 font-medium mt-1 ml-7">
              {description}
            </p>
          )}
        </div>
        {rightHeaderElement && (
          <div>
            {rightHeaderElement}
          </div>
        )}
      </div>

      {/* Chart Body Section */}
      <div className="flex-1 w-full min-h-[350px] relative mt-4">
        {loading ? (
          <div className="absolute inset-0 flex justify-center items-center bg-white/50 z-10">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600"></div>
          </div>
        ) : empty ? (
          <div className="absolute inset-0 flex justify-center items-center text-slate-400 font-bold border-2 border-dashed border-slate-100 rounded-2xl">
            {emptyMessage}
          </div>
        ) : (
          <div className="w-full h-full text-slate-800">
            {children}
          </div>
        )}
      </div>
    </div>
  );
}
