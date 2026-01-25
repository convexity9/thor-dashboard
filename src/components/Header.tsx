'use client';

import { useEffect, useState } from 'react';
import { SystemStatus } from '@/lib/supabase';

interface HeaderProps {
  status: SystemStatus | null;
  onRefresh: () => void;
  isRefreshing?: boolean;
}

export default function Header({ status, onRefresh, isRefreshing = false }: HeaderProps) {
  const [timeAgo, setTimeAgo] = useState<string>('');
  const [isStale, setIsStale] = useState(false);

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

  const getTimeAgo = (timestamp: string | null): string => {
    if (!timestamp) return 'never';
    let ts = timestamp.replace(' ', 'T');
    if (!ts.includes('Z') && !ts.includes('+') && !ts.includes('-', 10)) {
      ts = ts + 'Z';
    }
    const date = new Date(ts);
    const mins = Math.floor((Date.now() - date.getTime()) / 60000);
    if (mins < 1) return 'just now';
    if (mins < 60) return `${mins}m ago`;
    const hours = Math.floor(mins / 60);
    if (hours < 24) return `${hours}h ago`;
    return `${Math.floor(hours / 24)}d ago`;
  };

  // Update time ago every 30 seconds
  useEffect(() => {
    const updateTimeAgo = () => {
      const ago = getTimeAgo(status?.updated_at || null);
      setTimeAgo(ago);
      // Consider data stale if older than 20 minutes
      if (status?.updated_at) {
        let ts = status.updated_at.replace(' ', 'T');
        if (!ts.includes('Z') && !ts.includes('+') && !ts.includes('-', 10)) {
          ts = ts + 'Z';
        }
        const mins = (Date.now() - new Date(ts).getTime()) / 60000;
        setIsStale(mins > 20);
      }
    };
    updateTimeAgo();
    const interval = setInterval(updateTimeAgo, 30000);
    return () => clearInterval(interval);
  }, [status?.updated_at]);

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

            {/* Data Freshness Indicator */}
            <div className="flex items-center gap-3 text-sm">
              <div className="flex items-center gap-1.5">
                <span className={`h-2 w-2 rounded-full ${isStale ? 'bg-[var(--orange)] animate-pulse' : 'bg-[var(--green)]'}`} />
                <span className={isStale ? 'text-[var(--orange)]' : 'text-[var(--text-secondary)]'}>
                  {timeAgo || 'Loading...'}
                </span>
              </div>
              <span className="text-[var(--text-muted)]">•</span>
              <span className="text-[var(--text-secondary)]">
                Next: {formatTime(status?.next_scan_time || null)}
              </span>
            </div>

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
