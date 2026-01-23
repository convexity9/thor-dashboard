'use client';

import { Signal } from '@/lib/supabase';

interface SignalsTableProps {
  signals: Signal[];
}

export default function SignalsTable({ signals }: SignalsTableProps) {
  const formatPercent = (value: number | null) => {
    if (value === null) return '-';
    return `${(value * 100).toFixed(1)}%`;
  };

  const formatEdge = (value: number) => {
    const pct = (value * 100).toFixed(1);
    return value >= 0 ? `+${pct}%` : `${pct}%`;
  };

  const getActionColor = (action: string) => {
    switch (action) {
      case 'BUY':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'SELL':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      default:
        return 'bg-zinc-100 text-zinc-600 dark:bg-zinc-800 dark:text-zinc-400';
    }
  };

  return (
    <div className="rounded-lg border border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-900">
      <div className="border-b border-zinc-200 p-4 dark:border-zinc-800">
        <h2 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Recent Signals</h2>
        <p className="text-sm text-zinc-500 dark:text-zinc-400">Latest contract evaluations</p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="bg-zinc-50 dark:bg-zinc-800">
            <tr>
              <th className="px-4 py-3 text-left font-medium text-zinc-600 dark:text-zinc-400">Contract</th>
              <th className="px-4 py-3 text-left font-medium text-zinc-600 dark:text-zinc-400">City</th>
              <th className="px-4 py-3 text-right font-medium text-zinc-600 dark:text-zinc-400">GFS</th>
              <th className="px-4 py-3 text-right font-medium text-zinc-600 dark:text-zinc-400">ECMWF</th>
              <th className="px-4 py-3 text-right font-medium text-zinc-600 dark:text-zinc-400">Blended</th>
              <th className="px-4 py-3 text-right font-medium text-zinc-600 dark:text-zinc-400">Market</th>
              <th className="px-4 py-3 text-right font-medium text-zinc-600 dark:text-zinc-400">Edge</th>
              <th className="px-4 py-3 text-center font-medium text-zinc-600 dark:text-zinc-400">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-200 dark:divide-zinc-800">
            {signals.length === 0 ? (
              <tr>
                <td colSpan={8} className="px-4 py-8 text-center text-zinc-500">
                  No signals yet
                </td>
              </tr>
            ) : (
              signals.map((signal) => (
                <tr key={signal.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-800/50">
                  <td className="px-4 py-3">
                    <div className="font-medium text-zinc-900 dark:text-zinc-100">
                      {signal.threshold_temp}F
                    </div>
                    <div className="text-xs text-zinc-500">{signal.target_date}</div>
                  </td>
                  <td className="px-4 py-3 text-zinc-600 dark:text-zinc-400">{signal.city}</td>
                  <td className="px-4 py-3 text-right text-zinc-600 dark:text-zinc-400">
                    {formatPercent(signal.gfs_prob)}
                  </td>
                  <td className="px-4 py-3 text-right text-zinc-600 dark:text-zinc-400">
                    {formatPercent(signal.ecmwf_prob)}
                  </td>
                  <td className="px-4 py-3 text-right font-medium text-zinc-900 dark:text-zinc-100">
                    {formatPercent(signal.blended_prob)}
                  </td>
                  <td className="px-4 py-3 text-right text-zinc-600 dark:text-zinc-400">
                    {formatPercent(signal.market_price)}
                  </td>
                  <td className={`px-4 py-3 text-right font-medium ${
                    signal.edge >= 0.12 ? 'text-green-600' :
                    signal.edge <= -0.12 ? 'text-red-600' :
                    'text-zinc-600 dark:text-zinc-400'
                  }`}>
                    {formatEdge(signal.edge)}
                  </td>
                  <td className="px-4 py-3 text-center">
                    <span className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ${getActionColor(signal.action)}`}>
                      {signal.action}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
