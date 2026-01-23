'use client';

import { Signal } from '@/lib/supabase';

interface SignalsBarsProps {
  signals: Signal[];
}

export default function SignalsBars({ signals }: SignalsBarsProps) {
  // Filter to today's tradeable signals, sorted by absolute edge
  const today = new Date().toISOString().split('T')[0];
  const todaysSignals = signals
    .filter(s => s.timestamp.startsWith(today) && (s.action === 'BUY' || s.action === 'SELL'))
    .sort((a, b) => Math.abs(b.edge) - Math.abs(a.edge));

  const displaySignals = todaysSignals.slice(0, 6);
  const remainingCount = todaysSignals.length - 6;

  const formatEdge = (edge: number) => {
    const sign = edge >= 0 ? '+' : '';
    return `${sign}${(edge * 100).toFixed(1)}%`;
  };

  const formatProb = (prob: number | null) => {
    if (prob === null) return '—';
    return `${(prob * 100).toFixed(0)}%`;
  };

  const formatPrice = (price: number) => {
    return `$${price.toFixed(2)}`;
  };

  const getKalshiUrl = (ticker: string) => {
    // Extract event ticker (e.g., KXHIGHNY from KXHIGHNY-26JAN24-B18.5)
    const eventTicker = ticker.split('-')[0].toLowerCase();
    return `https://kalshi.com/markets/${eventTicker}`;
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
          const isPositive = signal.edge >= 0;

          return (
            <div
              key={signal.id}
              className="rounded-lg bg-[var(--bg-hover)] p-3"
            >
              {/* Top row: Contract name + Action badge */}
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-2">
                  <span className={`text-xs px-2 py-0.5 rounded font-bold ${
                    signal.action === 'BUY'
                      ? 'bg-[var(--green)]/20 text-[var(--green)]'
                      : 'bg-[var(--red)]/20 text-[var(--red)]'
                  }`}>
                    {signal.action}
                  </span>
                  <span className="text-sm font-medium text-[var(--text-primary)]">
                    {signal.city} {signal.threshold_temp}
                  </span>
                </div>
                <span className={`text-sm font-bold ${isPositive ? 'text-[var(--green)]' : 'text-[var(--red)]'}`}>
                  {formatEdge(signal.edge)} edge
                </span>
              </div>
              {/* Ticker link */}
              <a
                href={getKalshiUrl(signal.kalshi_ticker)}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-[var(--blue)] hover:underline mb-2 inline-block"
              >
                {signal.kalshi_ticker} ↗
              </a>

              {/* Bottom row: Key metrics */}
              <div className="grid grid-cols-4 gap-4 text-sm">
                <div>
                  <p className="text-xs text-[var(--text-secondary)]">Market</p>
                  <p className="text-[var(--text-primary)] font-medium">{formatPrice(signal.market_price)}</p>
                </div>
                <div>
                  <p className="text-xs text-[var(--text-secondary)]">Model</p>
                  <p className="text-[var(--text-primary)] font-medium">{formatProb(signal.blended_prob)}</p>
                </div>
                <div>
                  <p className="text-xs text-[var(--text-secondary)]">GFS</p>
                  <p className="text-[var(--text-primary)] font-medium">{formatProb(signal.gfs_prob)}</p>
                </div>
                <div>
                  <p className="text-xs text-[var(--text-secondary)]">ECMWF</p>
                  <p className="text-[var(--text-primary)] font-medium">{formatProb(signal.ecmwf_prob)}</p>
                </div>
              </div>
            </div>
          );
        })}

        {remainingCount > 0 && (
          <p className="text-sm text-[var(--text-muted)] text-center pt-2">
            +{remainingCount} more signals
          </p>
        )}
      </div>
    </div>
  );
}
