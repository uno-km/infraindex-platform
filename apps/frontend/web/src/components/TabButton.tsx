export default function TabButton({ 
  id, 
  active, 
  onClick, 
  children 
}: { 
  id: string; 
  active: string; 
  onClick: (id: string) => void; 
  children: React.ReactNode 
}) {
  const isActive = active === id;
  return (
    <button
      onClick={() => onClick(id)}
      className={`px-4 py-2 rounded-full font-semibold transition-all duration-300 ${
        isActive 
          ? "bg-white text-indigo-900 shadow-lg scale-105" 
          : "bg-white/10 text-white hover:bg-white/20"
      }`}
    >
      {children}
    </button>
  );
}
