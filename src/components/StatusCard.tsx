'use client';

import { SystemStatus } from '@/lib/supabase';

interface StatusCardProps {
  status: SystemStatus | null;
}

export default function StatusCard({ status }: StatusCardProps) {
  if (!status) {
    return (
      <div className="rounded-lg border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900">
        <h2 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">System Status</h2>
        <p className="mt-2 text-zinc-500">Loading...</p>
      </div>
    );
  }

  const formatTime = (timestamp: string | null) => {
    if (!timestamp) return 'Never';
    return new Date(timestamp).toLocaleString();
  };

  return (
    <div className="rounded-lg border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">System Status</h2>
        <span className={`rounded-full px-3 py-1 text-sm font-medium ${
          status.mode === 'paper'
            ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
            : 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
        }`}>
          {status.mode.toUpperCase()} MODE
        </span>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-4">
        <div className="flex items-center gap-2">
          <span className={`h-3 w-3 rounded-full ${status.kalshi_api_ok ? 'bg-green-500' : 'bg-red-500'}`} />
          <span className="text-sm text-zinc-600 dark:text-zinc-400">Kalshi API</span>
        </div>
        <div className="flex items-center gap-2">
          <span className={`h-3 w-3 rounded-full ${status.openmeteo_api_ok ? 'bg-green-500' : 'bg-red-500'}`} />
          <span className="text-sm text-zinc-600 dark:text-zinc-400">Open-Meteo API</span>
        </div>
      </div>

      {status.circuit_breaker_active && (
        <div className="mt-4 rounded-md bg-red-100 p-3 dark:bg-red-900/30">
          <p className="text-sm font-medium text-red-800 dark:text-red-200">
            Circuit Breaker Active: {status.circuit_breaker_reason}
          </p>
        </div>
      )}

      <div className="mt-4 space-y-2 text-sm text-zinc-600 dark:text-zinc-400">
        <p>Last Scan: {formatTime(status.last_scan_time)}</p>
        <p>Next Scan: {formatTime(status.next_scan_time)}</p>
        {status.forecast_age_hours !== null && (
          <p>Forecast Age: {status.forecast_age_hours.toFixed(1)} hours</p>
        )}
      </div>

      <div className="mt-4 border-t border-zinc-200 pt-4 dark:border-zinc-700">
        <div className="flex items-center justify-between text-sm">
          <span className="text-zinc-600 dark:text-zinc-400">Paper Trades</span>
          <span className="font-medium text-zinc-900 dark:text-zinc-100">
            {status.paper_trades_count} / {status.paper_target}
          </span>
        </div>
        <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-zinc-200 dark:bg-zinc-700">
          <div
            className="h-full bg-blue-500 transition-all"
            style={{ width: `${Math.min(100, (status.paper_trades_count / status.paper_target) * 100)}%` }}
          />
        </div>
      </div>
    </div>
  );
}
