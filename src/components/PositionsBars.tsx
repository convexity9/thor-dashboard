'use client';

import { Position } from '@/lib/supabase';

interface PositionsBarsProps {
  positions: Position[];
}

export default function PositionsBars({ positions }: PositionsBarsProps) {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
    }).format(value);
  };

  const formatPrice = (value: number | null) => {
    if (value === null) return '—';
    return `$${value.toFixed(2)}`;
  };

  const formatPnL = (value: number) => {
    const sign = value >= 0 ? '+' : '';
    return `${sign}${formatCurrency(value)}`;
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
          const pnl = position.unrealized_pnl ?? 0;
          const isProfitable = pnl >= 0;

          return (
            <div
              key={position.id}
              className="rounded-lg bg-[var(--bg-hover)] p-3"
            >
              {/* Top row: Contract name + Direction badge */}
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className={`text-xs px-2 py-0.5 rounded font-bold ${
                    position.direction === 'BUY'
                      ? 'bg-[var(--green)]/20 text-[var(--green)]'
                      : 'bg-[var(--red)]/20 text-[var(--red)]'
                  }`}>
                    {position.direction}
                  </span>
                  <span className="text-sm font-medium text-[var(--text-primary)]">
                    {position.city} {position.threshold_temp}
                  </span>
                </div>
                <span className="text-xs text-[var(--text-muted)]">
                  {position.target_date}
                </span>
              </div>

              {/* Bottom row: Key metrics */}
              <div className="grid grid-cols-4 gap-4 text-sm">
                <div>
                  <p className="text-xs text-[var(--text-muted)]">Contracts</p>
                  <p className="text-[var(--text-primary)] font-medium">{position.contracts}</p>
                </div>
                <div>
                  <p className="text-xs text-[var(--text-muted)]">Entry</p>
                  <p className="text-[var(--text-primary)] font-medium">{formatPrice(position.entry_price)}</p>
                </div>
                <div>
                  <p className="text-xs text-[var(--text-muted)]">Current</p>
                  <p className="text-[var(--text-primary)] font-medium">{formatPrice(position.current_price)}</p>
                </div>
                <div>
                  <p className="text-xs text-[var(--text-muted)]">Unrealized P&L</p>
                  <p className={`font-medium ${isProfitable ? 'text-[var(--green)]' : 'text-[var(--red)]'}`}>
                    {formatPnL(pnl)}
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
