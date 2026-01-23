'use client';

import { Position } from '@/lib/supabase';

interface PositionsTableProps {
  positions: Position[];
}

export default function PositionsTable({ positions }: PositionsTableProps) {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(value);
  };

  const formatPercent = (value: number) => {
    return `${(value * 100).toFixed(1)}%`;
  };

  return (
    <div className="rounded-lg border border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-900">
      <div className="border-b border-zinc-200 p-4 dark:border-zinc-800">
        <h2 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Open Positions</h2>
        <p className="text-sm text-zinc-500 dark:text-zinc-400">
          {positions.length} position{positions.length !== 1 ? 's' : ''} open
        </p>
      </div>

      {positions.length === 0 ? (
        <div className="p-8 text-center text-zinc-500">
          No open positions
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-zinc-50 dark:bg-zinc-800">
              <tr>
                <th className="px-4 py-3 text-left font-medium text-zinc-600 dark:text-zinc-400">Contract</th>
                <th className="px-4 py-3 text-left font-medium text-zinc-600 dark:text-zinc-400">Direction</th>
                <th className="px-4 py-3 text-right font-medium text-zinc-600 dark:text-zinc-400">Contracts</th>
                <th className="px-4 py-3 text-right font-medium text-zinc-600 dark:text-zinc-400">Entry</th>
                <th className="px-4 py-3 text-right font-medium text-zinc-600 dark:text-zinc-400">Current</th>
                <th className="px-4 py-3 text-right font-medium text-zinc-600 dark:text-zinc-400">Edge</th>
                <th className="px-4 py-3 text-right font-medium text-zinc-600 dark:text-zinc-400">Unrealized P&L</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-200 dark:divide-zinc-800">
              {positions.map((position) => (
                <tr key={position.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-800/50">
                  <td className="px-4 py-3">
                    <div className="font-medium text-zinc-900 dark:text-zinc-100">
                      {position.city} {position.threshold_temp}F
                    </div>
                    <div className="text-xs text-zinc-500">{position.target_date}</div>
                  </td>
                  <td className="px-4 py-3">
                    <span className={`inline-flex rounded-full px-2 py-1 text-xs font-medium ${
                      position.direction === 'BUY'
                        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                        : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                    }`}>
                      {position.direction}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-right text-zinc-600 dark:text-zinc-400">
                    {position.contracts}
                  </td>
                  <td className="px-4 py-3 text-right text-zinc-600 dark:text-zinc-400">
                    {formatCurrency(position.entry_price)}
                  </td>
                  <td className="px-4 py-3 text-right text-zinc-600 dark:text-zinc-400">
                    {position.current_price ? formatCurrency(position.current_price) : '-'}
                  </td>
                  <td className="px-4 py-3 text-right font-medium text-green-600">
                    {formatPercent(position.edge_at_entry)}
                  </td>
                  <td className={`px-4 py-3 text-right font-medium ${
                    position.unrealized_pnl >= 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {position.unrealized_pnl >= 0 ? '+' : ''}{formatCurrency(position.unrealized_pnl)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
