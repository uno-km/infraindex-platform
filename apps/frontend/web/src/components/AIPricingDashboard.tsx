import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, Legend, ResponsiveContainer, Step } from 'recharts';
import { Bot, Info, Loader2, RefreshCw } from "lucide-react";

interface AIModelPricing {
  id: string;
  model_code: string;
  name: string;
  provider: string;
  tier: string;
  context_length: number | null;
  input_price_1m: number;
  output_price_1m: number;
  collected_date: string;
}

export default function AIPricingDashboard() {
  const [latestData, setLatestData] = useState<Record<string, AIModelPricing[]>>({});
  const [historyData, setHistoryData] = useState<Record<string, any>>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchData = async () => {
    setLoading(true);
    try {
      const [latestRes, historyRes] = await Promise.all([
        fetch("http://localhost:8000/api/v1/ai-pricing/latest"),
        fetch("http://localhost:8000/api/v1/ai-pricing/history")
      ]);
      
      if (!latestRes.ok || !historyRes.ok) throw new Error("Failed to fetch API data");
      
      setLatestData(await latestRes.json());
      setHistoryData(await historyRes.json());
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Loader2 className="animate-spin text-indigo-500" size={32} />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 text-red-600 rounded-xl">
        Error loading AI Pricing Data: {error}
      </div>
    );
  }

  // Pre-process history data for recharts
  // We want an array of objects where each object is a date, and keys are model names.
  const chartDataByDate: Record<string, any> = {};
  
  Object.values(historyData).forEach((model: any) => {
    model.data.forEach((point: any) => {
      const date = point.date;
      if (!chartDataByDate[date]) {
        chartDataByDate[date] = { date };
      }
      // For charting, let's chart the average of input and output, or just input price.
      // Let's chart input price to keep it simple, or both. We will chart Input Price.
      chartDataByDate[date][model.name] = point.input_price;
    });
  });

  const chartDataArray = Object.values(chartDataByDate).sort((a: any, b: any) => 
    new Date(a.date).getTime() - new Date(b.date).getTime()
  );

  const colors = ["#8b5cf6", "#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#ec4899", "#6366f1", "#14b8a6"];
  const modelNames = Object.values(historyData).map((m: any) => m.name);

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex justify-between items-end">
        <div>
          <h2 className="text-3xl font-extrabold text-slate-800 tracking-tight flex items-center gap-3">
            <Bot className="text-indigo-600" size={32} />
            AI Token Pricing (1M Tokens)
          </h2>
          <p className="text-slate-500 mt-2">
            Real-time API pricing tracker for global AI models categorized by performance tiers.
          </p>
        </div>
        <button 
          onClick={fetchData}
          className="p-2.5 text-slate-500 hover:text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors border border-transparent hover:border-indigo-100"
        >
          <RefreshCw size={20} />
        </button>
      </div>

      {/* Chart Section */}
      <div className="bg-white rounded-3xl border border-slate-200/60 p-6 shadow-sm">
        <h3 className="text-lg font-bold text-slate-800 mb-6">Price History Trend (Input Price / 1M)</h3>
        <div className="h-96 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartDataArray}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
              <XAxis dataKey="date" tick={{fontSize: 12, fill: '#64748b'}} tickMargin={10} axisLine={false} tickLine={false} />
              <YAxis tick={{fontSize: 12, fill: '#64748b'}} tickMargin={10} axisLine={false} tickLine={false} tickFormatter={(value) => `$${value}`} />
              <RechartsTooltip 
                contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.1)' }}
              />
              <Legend wrapperStyle={{ paddingTop: '20px' }} />
              {modelNames.map((name, i) => (
                <Line 
                  key={name} 
                  type="stepAfter" 
                  dataKey={name} 
                  stroke={colors[i % colors.length]} 
                  strokeWidth={2}
                  dot={{ r: 4, strokeWidth: 2 }}
                  activeDot={{ r: 6 }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Tiers Tables Section */}
      <div className="space-y-6">
        {['Tier 0', 'Tier 1', 'Tier 2', 'Tier 3'].map((tier) => {
          const models = latestData[tier] || [];
          if (models.length === 0) return null;

          return (
            <div key={tier} className="bg-white rounded-3xl border border-slate-200/60 overflow-hidden shadow-sm">
              <div className="bg-slate-50 px-6 py-4 border-b border-slate-100 flex justify-between items-center">
                <h3 className="font-bold text-slate-800 flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-indigo-500"></div>
                  {tier} Models
                </h3>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="bg-white text-xs uppercase tracking-wider text-slate-500 border-b border-slate-100">
                      <th className="px-6 py-4 font-semibold">Provider</th>
                      <th className="px-6 py-4 font-semibold">Model Name</th>
                      <th className="px-6 py-4 font-semibold text-right">Input Price (1M)</th>
                      <th className="px-6 py-4 font-semibold text-right">Output Price (1M)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {models.map((model) => (
                      <tr key={model.id} className="hover:bg-slate-50/50 transition-colors">
                        <td className="px-6 py-4">
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-800">
                            {model.provider}
                          </span>
                        </td>
                        <td className="px-6 py-4 font-medium text-slate-800">{model.name}</td>
                        <td className="px-6 py-4 text-right text-emerald-600 font-semibold">${model.input_price_1m.toFixed(2)}</td>
                        <td className="px-6 py-4 text-right text-rose-600 font-semibold">${model.output_price_1m.toFixed(2)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
