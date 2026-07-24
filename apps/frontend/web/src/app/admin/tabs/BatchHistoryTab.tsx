import React, { useState, useEffect } from 'react';
import { Clock, CheckCircle, XCircle, AlertCircle, FileText } from 'lucide-react';
import { useAuth } from '../../../context/AuthContext';

export default function BatchHistoryTab() {
  const { token } = useAuth();
  const [histories, setHistories] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedError, setSelectedError] = useState<string | null>(null);

  useEffect(() => {
    fetchHistory();
  }, [token]);

  const fetchHistory = async () => {
    if (!token) return;
    try {
      setLoading(true);
      const res = await fetch('/api/v1/admin/batch/history?limit=100', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setHistories(data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const calculateDuration = (start: string, end: string) => {
    if (!start || !end) return '-';
    const ms = new Date(end).getTime() - new Date(start).getTime();
    return (ms / 1000).toFixed(1) + 's';
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Clock className="w-5 h-5 text-indigo-400" /> Batch Execution History
          </h2>
          <p className="text-sm text-gray-400 mt-1">Logs of all crawler batch DTL executions.</p>
        </div>
        <button 
          onClick={fetchHistory}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-bold rounded-lg transition-colors"
        >
          Refresh Data
        </button>
      </div>

      {loading ? (
        <div className="animate-pulse flex space-x-4">
          <div className="flex-1 space-y-4 py-1">
            <div className="h-4 bg-gray-800 rounded w-3/4"></div>
            <div className="space-y-2">
              <div className="h-4 bg-gray-800 rounded"></div>
              <div className="h-4 bg-gray-800 rounded w-5/6"></div>
            </div>
          </div>
        </div>
      ) : (
        <div className="overflow-x-auto rounded-xl border border-gray-800 bg-[#111]">
          <table className="w-full text-left text-sm">
            <thead className="bg-[#1a1a1a] text-gray-400 border-b border-gray-800 uppercase text-xs">
              <tr>
                <th className="px-4 py-3">SEQ</th>
                <th className="px-4 py-3">Master (BAT_ID)</th>
                <th className="px-4 py-3">Job (JOB_ID)</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">Start Time</th>
                <th className="px-4 py-3">Duration</th>
                <th className="px-4 py-3">Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800/50">
              {histories.map((h, i) => (
                <tr key={h.seq || i} className="hover:bg-white/5 transition-colors">
                  <td className="px-4 py-3 text-gray-500 font-mono">{h.seq}</td>
                  <td className="px-4 py-3 font-semibold text-gray-300">{h.bat_id}</td>
                  <td className="px-4 py-3 text-indigo-400">{h.job_id}</td>
                  <td className="px-4 py-3">
                    {h.status === 'SUCCESS' ? (
                      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-green-500/10 text-green-400 border border-green-500/20">
                        <CheckCircle className="w-3.5 h-3.5" /> SUCCESS
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-red-500/10 text-red-400 border border-red-500/20">
                        <XCircle className="w-3.5 h-3.5" /> FAIL
                      </span>
                    )}
                  </td>
                  <td className="px-4 py-3 text-gray-400 whitespace-nowrap">
                    {h.start_dt ? new Date(h.start_dt).toLocaleString() : '-'}
                  </td>
                  <td className="px-4 py-3 text-gray-400">
                    {calculateDuration(h.start_dt, h.end_dt)}
                  </td>
                  <td className="px-4 py-3">
                    {h.err_msg && (
                      <button
                        onClick={() => setSelectedError(h.err_msg)}
                        className="p-1.5 rounded-lg bg-red-500/10 text-red-400 hover:bg-red-500/20 transition-colors"
                        title="View Error Details"
                      >
                        <FileText className="w-4 h-4" />
                      </button>
                    )}
                  </td>
                </tr>
              ))}
              {histories.length === 0 && (
                <tr>
                  <td colSpan={7} className="px-4 py-8 text-center text-gray-500">
                    No history records found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* Error Modal */}
      {selectedError && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm">
          <div className="bg-[#111] border border-gray-800 rounded-2xl w-full max-w-4xl max-h-[80vh] flex flex-col shadow-2xl overflow-hidden">
            <div className="p-4 border-b border-gray-800 flex justify-between items-center bg-[#1a1a1a]">
              <h3 className="text-red-400 font-bold flex items-center gap-2">
                <AlertCircle className="w-5 h-5" /> Error Traceback
              </h3>
              <button 
                onClick={() => setSelectedError(null)}
                className="text-gray-400 hover:text-white"
              >
                Close
              </button>
            </div>
            <div className="p-4 overflow-y-auto bg-black flex-1">
              <pre className="text-red-400 text-xs font-mono whitespace-pre-wrap">
                {selectedError}
              </pre>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
