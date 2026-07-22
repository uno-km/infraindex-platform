import GpuDashboard from "../components/GpuDashboard";

export default function Home() {
  return (
    <main className="min-h-screen p-8 relative overflow-hidden">
      {/* Background decorations */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-[var(--color-cyber-purple)] opacity-10 blur-[120px] rounded-full pointer-events-none"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-[var(--color-cyber-neon)] opacity-10 blur-[120px] rounded-full pointer-events-none"></div>

      <div className="max-w-7xl mx-auto relative z-10">
        <header className="mb-12 flex justify-between items-end border-b border-white/10 pb-6">
          <div>
            <h1 className="text-4xl font-bold tracking-tighter text-white mb-2">
              Infra<span className="text-neon">Index</span>
            </h1>
            <p className="text-gray-400 text-sm tracking-wide uppercase">
              Global GPU Rental Intelligence
            </p>
          </div>
          <div className="text-right">
            <div className="inline-flex items-center gap-2 glass-panel px-4 py-2 rounded-full animate-pulse-glow">
              <span className="w-2 h-2 rounded-full bg-[var(--color-cyber-neon)] animate-ping"></span>
              <span className="text-xs text-neon font-semibold uppercase tracking-widest">Live Data</span>
            </div>
          </div>
        </header>

        <GpuDashboard />
      </div>
    </main>
  );
}
