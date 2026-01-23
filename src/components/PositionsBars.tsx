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

  const getKalshiUrl = (ticker: string) => {
    // Extract event ticker (e.g., KXHIGHNY from KXHIGHNY-26JAN24-B18.5)
    const eventTicker = ticker.split('-')[0].toLowerCase();
    return `https://kalshi.com/markets/${eventTicker}`;
  };

  // Calculate totals
  const totalIfWin = positions.reduce((sum, p) => {
    return sum + (p.direction === 'SELL'
      ? p.entry_price * p.contracts
      : (1 - p.entry_price) * p.contracts);
  }, 0);

  const totalIfLose = positions.reduce((sum, p) => {
    return sum + (p.direction === 'SELL'
      ? (1 - p.entry_price) * p.contracts
      : p.entry_price * p.contracts);
  }, 0);

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

      {/* Summary row */}
      <div className="flex justify-end gap-6 mb-4 pb-3 border-b border-[var(--border)]">
        <div className="text-right">
          <p className="text-xs text-[var(--text-secondary)]">Total If All Win</p>
          <p className="text-[var(--green)] font-bold">+{formatCurrency(totalIfWin)}</p>
        </div>
        <div className="text-right">
          <p className="text-xs text-[var(--text-secondary)]">Total If All Lose</p>
          <p className="text-[var(--red)] font-bold">-{formatCurrency(totalIfLose)}</p>
        </div>
      </div>

      <div className="space-y-3">
        {positions.map((position) => {
          return (
            <div
              key={position.id}
              className="rounded-lg bg-[var(--bg-hover)] p-3"
            >
              {/* Top row: Contract name + Direction badge */}
              <div className="flex items-center justify-between mb-1">
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
                  <span className="text-xs px-2 py-0.5 rounded bg-[var(--bg-primary)] text-[var(--text-secondary)]">
                    {new Date(position.target_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                  </span>
                </div>
              </div>
              {/* Ticker link */}
              <a
                href={getKalshiUrl(position.kalshi_ticker)}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-[var(--blue)] hover:underline mb-2 inline-block"
              >
                {position.kalshi_ticker} ↗
              </a>

              {/* Bottom row: Key metrics */}
              <div className="grid grid-cols-5 gap-3 text-sm">
                <div>
                  <p className="text-xs text-[var(--text-secondary)]">Contracts</p>
                  <p className="text-[var(--text-primary)] font-medium">{position.contracts}</p>
                </div>
                <div>
                  <p className="text-xs text-[var(--text-secondary)]">Entry</p>
                  <p className="text-[var(--text-primary)] font-medium">{formatPrice(position.entry_price)}</p>
                </div>
                <div>
                  <p className="text-xs text-[var(--text-secondary)]">Market Now</p>
                  <p className={`font-medium ${
                    position.current_price !== null
                      ? position.direction === 'SELL'
                        ? position.current_price < position.entry_price ? 'text-[var(--green)]' : 'text-[var(--red)]'
                        : position.current_price > position.entry_price ? 'text-[var(--green)]' : 'text-[var(--red)]'
                      : 'text-[var(--text-primary)]'
                  }`}>
                    {formatPrice(position.current_price)}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-[var(--text-secondary)]">If Win</p>
                  <p className="text-[var(--green)] font-medium">
                    +{formatCurrency(
                      position.direction === 'SELL'
                        ? position.entry_price * position.contracts
                        : (1 - position.entry_price) * position.contracts
                    )}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-[var(--text-secondary)]">If Lose</p>
                  <p className="text-[var(--red)] font-medium">
                    -{formatCurrency(
                      position.direction === 'SELL'
                        ? (1 - position.entry_price) * position.contracts
                        : position.entry_price * position.contracts
                    )}
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
