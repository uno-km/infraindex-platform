export default function FilterPanel() {
  return (
    <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-4 mb-6 shadow-sm">
      <h2 className="text-lg font-semibold mb-4">Filters</h2>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label className="block text-sm font-medium mb-1">Provider</label>
          <select className="w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-md p-2 text-sm">
            <option>All Providers</option>
            <option>Vast.ai</option>
            <option>Runpod</option>
            <option>AWS</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">GPU Model</label>
          <select className="w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-md p-2 text-sm">
            <option>All GPUs</option>
            <option>H100</option>
            <option>A100 80GB</option>
            <option>RTX 4090</option>
          </select>
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">GPU Count</label>
          <input type="number" min="1" placeholder="e.g. 8" className="w-full bg-gray-50 dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-md p-2 text-sm" />
        </div>
        <div className="flex items-end">
          <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-md p-2 transition-colors">
            Apply Filters
          </button>
        </div>
      </div>
    </div>
  );
}
