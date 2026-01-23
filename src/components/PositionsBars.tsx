'use client';

import { useState } from 'react';
import { Position } from '@/lib/supabase';

interface PositionsBarsProps {
  positions: Position[];
}

export default function PositionsBars({ positions }: PositionsBarsProps) {
  const [expandedId, setExpandedId] = useState<number | null>(null);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
    }).format(value);
  };

  const formatEdge = (edge: number) => {
    const sign = edge >= 0 ? '+' : '';
    return `${sign}${(edge * 100).toFixed(1)}%`;
  };

  // Determine if position is expected to profit
  // For BUY: positive edge = good (model says underpriced)
  // For SELL: negative edge = good (model says overpriced)
  const isPositionFavorable = (position: Position) => {
    if (position.direction === 'BUY') {
      return position.edge_at_entry > 0;
    } else {
      return position.edge_at_entry < 0;
    }
  };

  // Max edge for bar scaling
  const maxEdge = Math.max(...positions.map(p => Math.abs(p.edge_at_entry)), 0.2);

  const toggleExpand = (id: number) => {
    setExpandedId(expandedId === id ? null : id);
  };

  // Empty state
  if (positions.length === 0) {
    return (
      <div className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] p-5">
        <p className="text-sm text-[var(--text-secondary)] uppercase tracking-wide mb-4">
          Open Positions (0)
        </p>
        <div className="flex items-center justify-center h-32 text-[var(--text-muted)]">
          No open positions
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] p-5">
      <p className="text-sm text-[var(--text-secondary)] uppercase tracking-wide mb-4">
        Open Positions ({positions.length})
      </p>

      <div className="space-y-3">
        {positions.map((position) => {
          const favorable = isPositionFavorable(position);
          const barWidth = (Math.abs(position.edge_at_entry) / maxEdge) * 100;
          const isExpanded = expandedId === position.id;

          return (
            <div key={position.id}>
              <button
                onClick={() => toggleExpand(position.id)}
                className="w-full text-left hover:bg-[var(--bg-hover)] rounded-lg p-2 -m-2 transition-colors"
              >
                <div className="flex items-center gap-3">
                  {/* Contract name and direction badge */}
                  <div className="flex items-center gap-2 min-w-[180px]">
                    <span className={`text-xs px-1.5 py-0.5 rounded font-medium ${
                      position.direction === 'BUY'
                        ? 'bg-[var(--green)]/20 text-[var(--green)]'
                        : 'bg-[var(--red)]/20 text-[var(--red)]'
                    }`}>
                      {position.direction}
                    </span>
                    <span className="text-sm text-[var(--text-primary)] truncate">
                      {position.city} {position.threshold_temp}
                    </span>
                  </div>

                  {/* Bar */}
                  <div className="flex-1 h-4 bg-[var(--bg-hover)] rounded overflow-hidden">
                    <div
                      className={`h-full transition-all ${
                        favorable ? 'bg-[var(--green)]' : 'bg-[var(--red)]'
                      }`}
                      style={{ width: `${barWidth}%` }}
                    />
                  </div>

                  {/* Edge percentage */}
                  <span className={`text-sm font-medium min-w-[60px] text-right ${
                    favorable ? 'text-[var(--green)]' : 'text-[var(--red)]'
                  }`}>
                    {formatEdge(position.edge_at_entry)}
                  </span>
                </div>
              </button>

              {/* Expanded details */}
              {isExpanded && (
                <div className="mt-2 ml-2 pl-4 border-l-2 border-[var(--border)] text-sm text-[var(--text-secondary)] space-y-1">
                  <p><span className="text-[var(--text-muted)]">Ticker:</span> {position.kalshi_ticker}</p>
                  <p><span className="text-[var(--text-muted)]">Contracts:</span> {position.contracts}</p>
                  <p><span className="text-[var(--text-muted)]">Entry Price:</span> {formatCurrency(position.entry_price)}</p>
                  <p><span className="text-[var(--text-muted)]">Target Date:</span> {position.target_date}</p>
                  <p><span className="text-[var(--text-muted)]">Opened:</span> {new Date(position.opened_at).toLocaleString()}</p>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
