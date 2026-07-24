import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-50 w-full border-b border-gray-200 dark:border-gray-800 bg-white/50 dark:bg-black/50 backdrop-blur-md">
      <div className="container mx-auto flex h-16 items-center px-4 justify-between">
        <Link href="/" className="flex items-center gap-2">
          <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-teal-400">
            InfraIndex
          </span>
        </Link>
        <div className="flex gap-4">
          <Link href="/gpus" className="text-sm font-medium hover:text-blue-500 transition-colors">
            GPUs
          </Link>
          <Link href="/providers" className="text-sm font-medium hover:text-blue-500 transition-colors">
            Providers
          </Link>
        </div>
      </div>
    </nav>
  );
}
