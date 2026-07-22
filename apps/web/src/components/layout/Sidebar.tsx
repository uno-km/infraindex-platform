import Link from 'next/link';

export default function Sidebar() {
  return (
    <aside className="w-64 border-r border-gray-200 dark:border-gray-800 h-[calc(100vh-4rem)] sticky top-16 overflow-y-auto p-4 hidden md:block">
      <div className="space-y-6">
        <div>
          <h3 className="text-sm font-semibold mb-3 uppercase tracking-wider text-gray-500">Compute Index</h3>
          <ul className="space-y-2">
            <li><Link href="/" className="text-blue-500 font-medium">GPU Rental</Link></li>
            <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-500">CPU Compute</a></li>
            <li><a href="#" className="text-gray-600 dark:text-gray-400 hover:text-blue-500">Serverless</a></li>
          </ul>
        </div>
        <div>
          <h3 className="text-sm font-semibold mb-3 uppercase tracking-wider text-gray-500">Memory Index</h3>
          <ul className="space-y-2">
            <li><Link href="/memory" className="text-gray-600 dark:text-gray-400 hover:text-blue-500">Memory Index</Link></li>
            <li><Link href="/storage" className="text-gray-600 dark:text-gray-400 hover:text-blue-500">Storage Index</Link></li>
          </ul>
        </div>
      </div>
    </aside>
  );
}
