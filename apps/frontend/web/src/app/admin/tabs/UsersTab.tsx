"use client";

import React, { useState, useEffect } from 'react';
import { Users, History } from 'lucide-react';
import { useAuth } from '../../../context/AuthContext';

export default function UsersTab() {
  const { token } = useAuth();
  const [users, setUsers] = useState<any[]>([]);
  const [histories, setHistories] = useState<any[]>([]);
  const [view, setView] = useState<'users' | 'history'>('users');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!token) return;
    
    const fetchUsers = async () => {
      try {
        const res = await fetch('/api/v1/admin/users', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setUsers(data);
        }
      } catch (e) {
        console.error(e);
      }
    };

    const fetchHistory = async () => {
      try {
        const res = await fetch('/api/v1/admin/login-history', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setHistories(data);
        }
      } catch (e) {
        console.error(e);
      }
    };

    Promise.all([fetchUsers(), fetchHistory()]).then(() => setIsLoading(false));
  }, [token]);

  if (isLoading) return <div className="text-gray-400">Loading user data...</div>;

  return (
    <div className="space-y-6 text-white">
      <div className="flex gap-4 border-b border-gray-800 pb-4">
        <button 
          onClick={() => setView('users')}
          className={`font-semibold px-4 py-2 rounded-lg transition-colors flex items-center gap-2 ${view === 'users' ? 'bg-indigo-600 text-white' : 'text-gray-400 hover:bg-[#222]'}`}
        >
          <Users className="w-4 h-4" /> User List
        </button>
        <button 
          onClick={() => setView('history')}
          className={`font-semibold px-4 py-2 rounded-lg transition-colors flex items-center gap-2 ${view === 'history' ? 'bg-indigo-600 text-white' : 'text-gray-400 hover:bg-[#222]'}`}
        >
          <History className="w-4 h-4" /> Login History
        </button>
      </div>

      <div className="overflow-x-auto">
        {view === 'users' ? (
          <table className="w-full text-left text-sm text-gray-300">
            <thead className="bg-[#1a1a1a] text-gray-400 uppercase">
              <tr>
                <th className="px-4 py-3 rounded-tl-lg">ID / Email</th>
                <th className="px-4 py-3">Nickname</th>
                <th className="px-4 py-3">Provider</th>
                <th className="px-4 py-3">Role</th>
                <th className="px-4 py-3 rounded-tr-lg">Joined At</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id} className="border-b border-gray-800 hover:bg-[#1a1a1a]/50">
                  <td className="px-4 py-3 font-mono">{u.email || u.id.slice(0, 13) + '...'}</td>
                  <td className="px-4 py-3 font-semibold">{u.nickname}</td>
                  <td className="px-4 py-3 capitalize">{u.oauth_provider || 'Local'}</td>
                  <td className="px-4 py-3">
                    {u.is_admin ? <span className="text-red-400 font-bold">Admin</span> : <span>User</span>}
                  </td>
                  <td className="px-4 py-3">{u.created_at ? new Date(u.created_at).toLocaleString() : '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <table className="w-full text-left text-sm text-gray-300">
            <thead className="bg-[#1a1a1a] text-gray-400 uppercase">
              <tr>
                <th className="px-4 py-3 rounded-tl-lg">User Nickname</th>
                <th className="px-4 py-3">Method</th>
                <th className="px-4 py-3">IP Address</th>
                <th className="px-4 py-3">User Agent</th>
                <th className="px-4 py-3 rounded-tr-lg">Login Time</th>
              </tr>
            </thead>
            <tbody>
              {histories.map((h) => (
                <tr key={h.id} className="border-b border-gray-800 hover:bg-[#1a1a1a]/50">
                  <td className="px-4 py-3 font-semibold">{h.nickname}</td>
                  <td className="px-4 py-3 capitalize text-indigo-400">{h.login_method}</td>
                  <td className="px-4 py-3 font-mono text-xs">{h.ip_address || '-'}</td>
                  <td className="px-4 py-3 text-xs truncate max-w-[200px]" title={h.user_agent}>{h.user_agent || '-'}</td>
                  <td className="px-4 py-3">{h.created_at ? new Date(h.created_at).toLocaleString() : '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
