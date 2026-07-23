"use client";

import React, { useState, useEffect } from 'react';
import { Bell, Search, Filter, Plus, Trash2, CheckCircle, Clock, AlertTriangle, ExternalLink } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import Header from './layout/Header';
import Sidebar from './layout/Sidebar';

// Types
interface AlertRule {
  id: string;
  target: string;
  alert_type: string;
  price_threshold?: number;
  is_active: boolean;
}

interface AlertHistory {
  id: string;
  title: string;
  message: string;
  link_url?: string;
  is_read: boolean;
  created_at: string;
}

export default function AlertsDashboard() {
  const { isAuthenticated, user, token } = useAuth();
  
  const [activeTab, setActiveTab] = useState<'history' | 'rules'>('history');
  const [history, setHistory] = useState<AlertHistory[]>([]);
  const [rules, setRules] = useState<AlertRule[]>([]);
  
  const [isRuleModalOpen, setIsRuleModalOpen] = useState(false);
  const [newRuleForm, setNewRuleForm] = useState({
    target: '',
    alert_type: 'retail_price',
    price_threshold: ''
  });

  const fetchHistory = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/alerts/history', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setHistory(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const fetchRules = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/v1/alerts/rules', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setRules(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      fetchHistory();
      fetchRules();
    }
  }, [isAuthenticated, token]);

  const handleMarkAsRead = async (id: string) => {
    try {
      const res = await fetch(`http://localhost:8000/api/v1/alerts/history/${id}/read`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        fetchHistory();
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleCreateRule = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload: any = {
        target: newRuleForm.target,
        alert_type: newRuleForm.alert_type,
        is_active: true
      };
      
      if (newRuleForm.alert_type === 'retail_price' && newRuleForm.price_threshold) {
        payload.price_threshold = parseFloat(newRuleForm.price_threshold);
      }
      
      const res = await fetch('http://localhost:8000/api/v1/alerts/rules', {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });
      
      if (res.ok) {
        setIsRuleModalOpen(false);
        setNewRuleForm({ target: '', alert_type: 'retail_price', price_threshold: '' });
        fetchRules();
      }
    } catch (e) {
      console.error(e);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="flex flex-col min-h-screen bg-slate-50">
        <Header searchQuery="" setSearchQuery={() => {}} />
        <div className="flex-1 flex items-center justify-center">
          <div className="bg-white p-8 rounded-2xl shadow-sm text-center max-w-md">
            <Bell size={48} className="mx-auto text-slate-300 mb-4" />
            <h2 className="text-xl font-bold text-slate-800 mb-2">로그인이 필요합니다</h2>
            <p className="text-slate-500 mb-6">맞춤형 알림 대시보드를 사용하시려면 먼저 로그인해주세요.</p>
            <button 
              onClick={() => window.dispatchEvent(new CustomEvent('open-login-modal'))}
              className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3 px-6 rounded-xl w-full transition-colors"
            >
              로그인하기
            </button>
          </div>
        </div>
      </div>
    );
  }

  const unreadCount = history.filter(h => !h.is_read).length;

  return (
    <div className="flex flex-col min-h-screen bg-slate-50">
      <Header searchQuery="" setSearchQuery={() => {}} />
      
      <div className="flex-1 flex max-w-[1600px] w-full mx-auto">
        <Sidebar selectedCategory="dashboard" setSelectedCategory={() => {}} />
        
        <main className="flex-1 p-6 lg:p-10 overflow-y-auto">
          <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4">
            <div>
              <h1 className="text-3xl font-black text-slate-900 tracking-tight flex items-center gap-3">
                <Bell className="text-indigo-600" size={32} strokeWidth={2.5} />
                맞춤형 알림 대시보드
              </h1>
              <p className="text-slate-500 mt-2 font-medium">
                설정한 가격 변동 및 키워드 알림 내역을 한눈에 확인하세요.
              </p>
            </div>
            
            <button 
              onClick={() => setIsRuleModalOpen(true)}
              className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-3 rounded-xl font-bold transition-all shadow-md hover:shadow-lg self-start md:self-auto"
            >
              <Plus size={20} />
              새 알림 추가
            </button>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-200/60 flex items-center gap-5">
              <div className="w-14 h-14 rounded-full bg-red-100 flex items-center justify-center flex-shrink-0">
                <Bell size={24} className="text-red-600" />
              </div>
              <div>
                <p className="text-sm font-bold text-slate-500 uppercase tracking-wider mb-1">안 읽은 알림</p>
                <h3 className="text-3xl font-black text-slate-800">{unreadCount}<span className="text-lg font-bold text-slate-400 ml-1">건</span></h3>
              </div>
            </div>
            
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-200/60 flex items-center gap-5">
              <div className="w-14 h-14 rounded-full bg-indigo-100 flex items-center justify-center flex-shrink-0">
                <Filter size={24} className="text-indigo-600" />
              </div>
              <div>
                <p className="text-sm font-bold text-slate-500 uppercase tracking-wider mb-1">활성 알림 규칙</p>
                <h3 className="text-3xl font-black text-slate-800">{rules.filter(r => r.is_active).length}<span className="text-lg font-bold text-slate-400 ml-1">개</span></h3>
              </div>
            </div>
          </div>

          {/* Tabs */}
          <div className="flex border-b border-slate-200 mb-6">
            <button
              onClick={() => setActiveTab('history')}
              className={`pb-4 px-6 font-bold text-sm transition-colors border-b-2 ${
                activeTab === 'history' 
                  ? 'border-indigo-600 text-indigo-700' 
                  : 'border-transparent text-slate-500 hover:text-slate-700'
              }`}
            >
              알림 내역
            </button>
            <button
              onClick={() => setActiveTab('rules')}
              className={`pb-4 px-6 font-bold text-sm transition-colors border-b-2 ${
                activeTab === 'rules' 
                  ? 'border-indigo-600 text-indigo-700' 
                  : 'border-transparent text-slate-500 hover:text-slate-700'
              }`}
            >
              알림 규칙 설정
            </button>
          </div>

          {/* History Tab */}
          {activeTab === 'history' && (
            <div className="space-y-4">
              {history.length === 0 ? (
                <div className="bg-white p-10 rounded-2xl border border-slate-200/60 text-center">
                  <Clock size={40} className="mx-auto text-slate-300 mb-4" />
                  <p className="text-slate-500 font-medium">발생한 알림 내역이 없습니다.</p>
                </div>
              ) : (
                history.map((alert) => (
                  <div 
                    key={alert.id} 
                    className={`bg-white p-6 rounded-2xl border transition-all ${
                      alert.is_read 
                        ? 'border-slate-200/60 opacity-75' 
                        : 'border-indigo-200 shadow-sm shadow-indigo-100 ring-1 ring-indigo-50'
                    }`}
                  >
                    <div className="flex justify-between items-start gap-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          {!alert.is_read && (
                            <span className="w-2.5 h-2.5 bg-red-500 rounded-full"></span>
                          )}
                          <h3 className={`text-lg font-bold ${alert.is_read ? 'text-slate-700' : 'text-slate-900'}`}>
                            {alert.title}
                          </h3>
                          <span className="text-xs font-medium text-slate-400 bg-slate-100 px-2 py-1 rounded-md">
                            {new Date(alert.created_at).toLocaleString()}
                          </span>
                        </div>
                        <p className={`text-sm ${alert.is_read ? 'text-slate-500' : 'text-slate-600 font-medium'}`}>
                          {alert.message}
                        </p>
                      </div>
                      
                      <div className="flex items-center gap-3 flex-shrink-0">
                        {alert.link_url && (
                          <a 
                            href={alert.link_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
                            title="자세히 보기"
                          >
                            <ExternalLink size={20} />
                          </a>
                        )}
                        {!alert.is_read && (
                          <button 
                            onClick={() => handleMarkAsRead(alert.id)}
                            className="p-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors flex items-center gap-2 text-sm font-bold"
                          >
                            <CheckCircle size={20} />
                            <span className="hidden sm:inline">확인</span>
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}

          {/* Rules Tab */}
          {activeTab === 'rules' && (
            <div className="bg-white rounded-2xl border border-slate-200/60 overflow-hidden">
              {rules.length === 0 ? (
                <div className="p-10 text-center">
                  <Filter size={40} className="mx-auto text-slate-300 mb-4" />
                  <p className="text-slate-500 font-medium mb-4">설정된 알림 규칙이 없습니다.</p>
                  <button 
                    onClick={() => setIsRuleModalOpen(true)}
                    className="text-indigo-600 font-bold hover:underline"
                  >
                    새 규칙 추가하기
                  </button>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-left">
                    <thead className="bg-slate-50 border-b border-slate-200">
                      <tr>
                        <th className="py-4 px-6 text-sm font-bold text-slate-600">유형</th>
                        <th className="py-4 px-6 text-sm font-bold text-slate-600">대상(키워드)</th>
                        <th className="py-4 px-6 text-sm font-bold text-slate-600">조건</th>
                        <th className="py-4 px-6 text-sm font-bold text-slate-600">상태</th>
                        <th className="py-4 px-6 text-sm font-bold text-slate-600 text-right">관리</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-200">
                      {rules.map((rule) => (
                        <tr key={rule.id} className="hover:bg-slate-50 transition-colors">
                          <td className="py-4 px-6">
                            <span className={`inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold ${
                              rule.alert_type === 'retail_price' ? 'bg-blue-100 text-blue-700' : 'bg-purple-100 text-purple-700'
                            }`}>
                              {rule.alert_type === 'retail_price' ? '가격 알림' : '뉴스 키워드'}
                            </span>
                          </td>
                          <td className="py-4 px-6 text-sm font-bold text-slate-800">{rule.target}</td>
                          <td className="py-4 px-6 text-sm text-slate-600 font-medium">
                            {rule.alert_type === 'retail_price' 
                              ? `₩${rule.price_threshold?.toLocaleString()} 이하`
                              : '포함시 알림'}
                          </td>
                          <td className="py-4 px-6">
                            <span className={`inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold ${
                              rule.is_active ? 'bg-green-100 text-green-700' : 'bg-slate-100 text-slate-500'
                            }`}>
                              {rule.is_active ? '활성' : '비활성'}
                            </span>
                          </td>
                          <td className="py-4 px-6 text-right">
                            <button className="text-red-500 hover:text-red-700 p-2 rounded-lg hover:bg-red-50 transition-colors">
                              <Trash2 size={18} />
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}
        </main>
      </div>

      {/* Create Rule Modal */}
      {isRuleModalOpen && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center z-[100] p-4">
          <div className="bg-white rounded-3xl w-full max-w-lg shadow-2xl overflow-hidden animate-in fade-in zoom-in duration-200">
            <div className="p-6 md:p-8">
              <h2 className="text-2xl font-black text-slate-800 mb-6">새 알림 규칙 추가</h2>
              
              <form onSubmit={handleCreateRule} className="space-y-5">
                <div>
                  <label className="block text-sm font-bold text-slate-700 mb-2">알림 유형</label>
                  <div className="grid grid-cols-2 gap-3">
                    <button
                      type="button"
                      onClick={() => setNewRuleForm({...newRuleForm, alert_type: 'retail_price'})}
                      className={`py-3 px-4 rounded-xl border-2 font-bold transition-all text-sm ${
                        newRuleForm.alert_type === 'retail_price'
                          ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                          : 'border-slate-200 bg-white text-slate-600 hover:border-slate-300'
                      }`}
                    >
                      가격 변동 알림
                    </button>
                    <button
                      type="button"
                      onClick={() => setNewRuleForm({...newRuleForm, alert_type: 'news_keyword'})}
                      className={`py-3 px-4 rounded-xl border-2 font-bold transition-all text-sm ${
                        newRuleForm.alert_type === 'news_keyword'
                          ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                          : 'border-slate-200 bg-white text-slate-600 hover:border-slate-300'
                      }`}
                    >
                      뉴스 키워드 알림
                    </button>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-bold text-slate-700 mb-2">
                    {newRuleForm.alert_type === 'retail_price' ? '대상 상품 (예: RTX 4090)' : '추적 키워드 (예: HBM3E)'}
                  </label>
                  <input 
                    type="text" 
                    required
                    value={newRuleForm.target}
                    onChange={(e) => setNewRuleForm({...newRuleForm, target: e.target.value})}
                    className="w-full bg-slate-50 border border-slate-300 focus:bg-white focus:border-indigo-600 focus:ring-4 focus:ring-indigo-100 rounded-xl py-3 px-4 text-slate-800 font-medium outline-none transition-all"
                    placeholder="입력해주세요"
                  />
                </div>

                {newRuleForm.alert_type === 'retail_price' && (
                  <div>
                    <label className="block text-sm font-bold text-slate-700 mb-2">목표 가격 (원)</label>
                    <div className="relative">
                      <input 
                        type="number" 
                        required
                        value={newRuleForm.price_threshold}
                        onChange={(e) => setNewRuleForm({...newRuleForm, price_threshold: e.target.value})}
                        className="w-full bg-slate-50 border border-slate-300 focus:bg-white focus:border-indigo-600 focus:ring-4 focus:ring-indigo-100 rounded-xl py-3 px-4 text-slate-800 font-medium outline-none transition-all pl-10"
                        placeholder="2200000"
                      />
                      <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 font-bold">₩</span>
                    </div>
                    <p className="text-xs text-slate-500 mt-2">입력하신 가격 이하로 떨어지면 알림을 받습니다.</p>
                  </div>
                )}
                
                <div className="pt-4 flex gap-3">
                  <button 
                    type="button"
                    onClick={() => setIsRuleModalOpen(false)}
                    className="flex-1 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold py-3.5 px-4 rounded-xl transition-colors"
                  >
                    취소
                  </button>
                  <button 
                    type="submit"
                    className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3.5 px-4 rounded-xl transition-colors"
                  >
                    추가하기
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
