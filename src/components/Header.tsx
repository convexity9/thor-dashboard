'use client';

import { SystemStatus } from '@/lib/supabase';

interface HeaderProps {
  status: SystemStatus | null;
  onRefresh: () => void;
  isRefreshing?: boolean;
}

export default function Header({ status, onRefresh, isRefreshing = false }: HeaderProps) {
  const formatTime = (timestamp: string | null) => {
    if (!timestamp) return 'Never';
    // Supabase timestamps are UTC - normalize format and ensure proper parsing
    let ts = timestamp.replace(' ', 'T'); // Handle "2025-01-23 15:20:00" format
    if (!ts.includes('Z') && !ts.includes('+') && !ts.includes('-', 10)) {
      ts = ts + 'Z'; // Append Z to treat as UTC
    }
    const date = new Date(ts);
    return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
  };

  return (
    <>
      <header className="border-b border-[var(--border)] bg-[var(--bg-card)] px-6 py-4">
        <div className="mx-auto max-w-7xl flex items-center justify-between">
          <div className="flex items-center gap-8">
            <h1 className="text-xl font-bold text-[var(--text-primary)]">THOR</h1>

            {/* API Status Indicators */}
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <span className={`h-2 w-2 rounded-full ${status?.kalshi_api_ok ? 'bg-[var(--green)]' : 'bg-[var(--red)]'}`} />
                <span className="text-xs text-[var(--text-secondary)]">Kalshi</span>
              </div>
              <div className="flex items-center gap-2">
                <span className={`h-2 w-2 rounded-full ${status?.openmeteo_api_ok ? 'bg-[var(--green)]' : 'bg-[var(--red)]'}`} />
                <span className="text-xs text-[var(--text-secondary)]">OpenMeteo</span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-6">
            {/* Mode Badge */}
            <span className={`rounded px-3 py-1 text-xs font-bold tracking-wider ${
              status?.mode === 'paper'
                ? 'bg-[var(--orange)]/20 text-[var(--orange)]'
                : 'bg-[var(--green)]/20 text-[var(--green)]'
            }`}>
              {status?.mode?.toUpperCase() || 'PAPER'}
            </span>

            {/* Last Scan Time */}
            <span className="text-sm text-[var(--text-secondary)]">
              Last: {formatTime(status?.last_scan_time || null)}
            </span>

            {/* Refresh Button */}
            <button
              type="button"
              onClick={onRefresh}
              disabled={isRefreshing}
              className="rounded bg-[var(--bg-hover)] px-3 py-1.5 text-sm text-[var(--text-secondary)] hover:bg-[var(--border)] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isRefreshing ? 'Refreshing...' : 'Refresh'}
            </button>
          </div>
        </div>
      </header>

      {/* Circuit Breaker Alert Banner */}
      {status?.circuit_breaker_active && (
        <div className="bg-[var(--red)]/20 border-b border-[var(--red)]/30 px-6 py-3">
          <div className="mx-auto max-w-7xl flex items-center gap-3">
            <span className="text-lg">⚠️</span>
            <div>
              <span className="font-semibold text-[var(--red)]">CIRCUIT BREAKER ACTIVE</span>
              <span className="text-[var(--text-secondary)]"> — Trading paused: {status.circuit_breaker_reason}</span>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
