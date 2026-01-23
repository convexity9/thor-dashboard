'use client';

import { useState } from 'react';
import { Signal } from '@/lib/supabase';

interface SignalsBarsProps {
  signals: Signal[];
}

export default function SignalsBars({ signals }: SignalsBarsProps) {
  const [expandedId, setExpandedId] = useState<number | null>(null);

  // Filter to today's signals and sort by absolute edge
  const today = new Date().toISOString().split('T')[0];
  const todaysSignals = signals
    .filter(s => s.timestamp.startsWith(today) && (s.action === 'BUY' || s.action === 'SELL'))
    .sort((a, b) => Math.abs(b.edge) - Math.abs(a.edge));

  const displaySignals = todaysSignals.slice(0, 5);
  const remainingCount = todaysSignals.length - 5;

  const formatEdge = (edge: number) => {
    const sign = edge >= 0 ? '+' : '';
    return `${sign}${(edge * 100).toFixed(0)}%`;
  };

  const formatProb = (prob: number | null) => {
    if (prob === null) return 'N/A';
    return `${(prob * 100).toFixed(1)}%`;
  };

  // Max edge for bar scaling
  const maxEdge = Math.max(...displaySignals.map(s => Math.abs(s.edge)), 0.2);

  const toggleExpand = (id: number) => {
    setExpandedId(expandedId === id ? null : id);
  };

  // Empty state
  if (todaysSignals.length === 0) {
    return (
      <div className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] p-5">
        <p className="text-sm text-[var(--text-secondary)] uppercase tracking-wide mb-4">
          Signals Today (0)
        </p>
        <div className="flex items-center justify-center h-32 text-[var(--text-muted)]">
          Awaiting next scan
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] p-5">
      <p className="text-sm text-[var(--text-secondary)] uppercase tracking-wide mb-4">
        Signals Today ({todaysSignals.length})
      </p>

      <div className="space-y-3">
        {displaySignals.map((signal) => {
          const barWidth = (Math.abs(signal.edge) / maxEdge) * 100;
          const isExpanded = expandedId === signal.id;
          const isPositive = signal.edge >= 0;

          return (
            <div key={signal.id}>
              <button
                onClick={() => toggleExpand(signal.id)}
                className="w-full text-left hover:bg-[var(--bg-hover)] rounded-lg p-2 -m-2 transition-colors"
              >
                <div className="flex items-center gap-3">
                  {/* Contract name */}
                  <span className="text-sm text-[var(--text-primary)] min-w-[140px] truncate">
                    {signal.city} {signal.threshold_temp}
                  </span>

                  {/* Bar */}
                  <div className="flex-1 h-4 bg-[var(--bg-hover)] rounded overflow-hidden">
                    <div
                      className={`h-full transition-all ${
                        isPositive ? 'bg-[var(--green)]' : 'bg-[var(--red)]'
                      }`}
                      style={{ width: `${barWidth}%` }}
                    />
                  </div>

                  {/* Edge percentage */}
                  <span className={`text-sm font-medium min-w-[50px] text-right ${
                    isPositive ? 'text-[var(--green)]' : 'text-[var(--red)]'
                  }`}>
                    {formatEdge(signal.edge)}
                  </span>
                </div>
              </button>

              {/* Expanded details */}
              {isExpanded && (
                <div className="mt-2 ml-2 pl-4 border-l-2 border-[var(--border)] text-sm text-[var(--text-secondary)] space-y-1">
                  <p><span className="text-[var(--text-muted)]">Action:</span> {signal.action}</p>
                  <p><span className="text-[var(--text-muted)]">Ticker:</span> {signal.kalshi_ticker}</p>
                  <p><span className="text-[var(--text-muted)]">GFS:</span> {formatProb(signal.gfs_prob)}</p>
                  <p><span className="text-[var(--text-muted)]">ECMWF:</span> {formatProb(signal.ecmwf_prob)}</p>
                  <p><span className="text-[var(--text-muted)]">Blended:</span> {formatProb(signal.blended_prob)}</p>
                  <p><span className="text-[var(--text-muted)]">Market:</span> {formatProb(signal.market_price)}</p>
                  {signal.skip_reason && (
                    <p><span className="text-[var(--text-muted)]">Skip Reason:</span> {signal.skip_reason}</p>
                  )}
                </div>
              )}
            </div>
          );
        })}

        {remainingCount > 0 && (
          <p className="text-sm text-[var(--text-muted)] pl-2">
            +{remainingCount} more
          </p>
        )}
      </div>
    </div>
  );
}
