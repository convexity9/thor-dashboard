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

  const formatProb = (value: number | null) => {
    if (value === null) return '—';
    return `${(value * 100).toFixed(0)}%`;
  };

  const getKalshiUrl = (ticker: string) => {
    const eventTicker = ticker.split('-')[0].toLowerCase();
    return `https://kalshi.com/markets/${eventTicker}`;
  };

  // Calculate win probability (inverted for SELL positions)
  const getWinProb = (position: Position): number | null => {
    if (position.model_prob === null) return null;
    return position.direction === 'SELL'
      ? 1 - position.model_prob
      : position.model_prob;
  };

  // Calculate totals
  // entry_price now correctly represents what we paid (YES price for BUY, NO price for SELL)
  // If Win: contract pays $1, profit = $1 - entry_price
  // If Lose: contract pays $0, loss = entry_price
  const totalIfWin = positions.reduce((sum, p) => {
    return sum + (1 - p.entry_price) * p.contracts;
  }, 0);

  const totalIfLose = positions.reduce((sum, p) => {
    return sum + p.entry_price * p.contracts;
  }, 0);

  // Calculate model-based expected value using WIN probability
  // For each position: expected = winProb * win_amount - (1-winProb) * loss_amount
  const positionsWithProb = positions.filter(p => p.model_prob !== null);

  const expectedPnL = positionsWithProb.reduce((sum, p) => {
    const winProb = getWinProb(p)!;
    const winAmount = (1 - p.entry_price) * p.contracts;
    const loseAmount = p.entry_price * p.contracts;
    return sum + (winProb * winAmount) - ((1 - winProb) * loseAmount);
  }, 0);

  // Average WIN probability (weighted by position size)
  const totalPositionValue = positionsWithProb.reduce((sum, p) =>
    sum + p.entry_price * p.contracts, 0);

  const weightedAvgWinProb = totalPositionValue > 0
    ? positionsWithProb.reduce((sum, p) => {
        const weight = (p.entry_price * p.contracts) / totalPositionValue;
        return sum + (getWinProb(p)! * weight);
      }, 0)
    : null;

  // Expected wins (sum of win probabilities)
  const expectedWins = positionsWithProb.reduce((sum, p) => sum + getWinProb(p)!, 0);

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
      <div className="grid grid-cols-2 gap-4 mb-4 pb-3 border-b border-[var(--border)]">
        {/* Model expectations */}
        <div className="flex gap-4">
          {weightedAvgWinProb !== null && (
            <div>
              <p className="text-xs text-[var(--text-secondary)]">Avg Win Prob</p>
              <p className="text-[var(--text-primary)] font-bold">{formatProb(weightedAvgWinProb)}</p>
            </div>
          )}
          {positionsWithProb.length > 0 && (
            <div>
              <p className="text-xs text-[var(--text-secondary)]">Expected Wins</p>
              <p className="text-[var(--text-primary)] font-bold">{expectedWins.toFixed(1)} / {positions.length}</p>
            </div>
          )}
          {positionsWithProb.length > 0 && (
            <div>
              <p className="text-xs text-[var(--text-secondary)]">Expected P&L</p>
              <p className={`font-bold ${expectedPnL >= 0 ? 'text-[var(--green)]' : 'text-[var(--red)]'}`}>
                {expectedPnL >= 0 ? '+' : ''}{formatCurrency(expectedPnL)}
              </p>
            </div>
          )}
        </div>
        {/* Outcome scenarios */}
        <div className="flex justify-end gap-4">
          <div className="text-right">
            <p className="text-xs text-[var(--text-secondary)]">Total Allocated</p>
            <p className="text-[var(--text-primary)] font-bold">{formatCurrency(totalIfLose)}</p>
          </div>
          <div className="text-right">
            <p className="text-xs text-[var(--text-secondary)]">If All Win</p>
            <p className="text-[var(--green)] font-bold">+{formatCurrency(totalIfWin)}</p>
          </div>
          <div className="text-right">
            <p className="text-xs text-[var(--text-secondary)]">If All Lose</p>
            <p className="text-[var(--red)] font-bold">-{formatCurrency(totalIfLose)}</p>
          </div>
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
                    {new Date(position.target_date + 'T12:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                  </span>
                </div>
                {/* Win probability badge */}
                {position.model_prob !== null && (
                  <span className={`text-sm font-bold ${
                    getWinProb(position)! >= 0.7 ? 'text-[var(--green)]' :
                    getWinProb(position)! >= 0.5 ? 'text-[var(--text-primary)]' :
                    'text-[var(--red)]'
                  }`}>
                    {formatProb(getWinProb(position))} win
                  </span>
                )}
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
                  <p className="text-xs text-[var(--text-secondary)]">Allocated</p>
                  <p className="text-[var(--text-primary)] font-medium">
                    {formatCurrency(position.entry_price * position.contracts)}
                  </p>
                  <p className="text-xs text-[var(--text-secondary)]">{position.contracts.toLocaleString()} contracts</p>
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
                    +{formatCurrency((1 - position.entry_price) * position.contracts)}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-[var(--text-secondary)]">If Lose</p>
                  <p className="text-[var(--red)] font-medium">
                    -{formatCurrency(position.entry_price * position.contracts)}
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
