'use client';

import { SystemStatus, Trade } from '@/lib/supabase';

interface WinRateCardProps {
  status: SystemStatus | null;
  trades: Trade[];
}

export default function WinRateCard({ status, trades }: WinRateCardProps) {
  const resolvedTrades = trades.length;
  const wins = trades.filter(t => t.result === 'win').length;
  const losses = trades.filter(t => t.result === 'loss').length;

  // Show win rate if 10+ resolved trades, otherwise show fill rate
  const showWinRate = resolvedTrades >= 10;

  const winRate = resolvedTrades > 0 ? (wins / resolvedTrades) * 100 : 0;
  const fillRate = status?.fill_rate ? status.fill_rate * 100 : 0;
  const targetWinRate = 54;

  const displayRate = showWinRate ? winRate : fillRate;
  const meetsTarget = showWinRate && winRate >= targetWinRate;

  return (
    <div className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] p-5">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-[var(--text-secondary)] uppercase tracking-wide">
            {showWinRate ? 'Win Rate' : 'Fill Rate'}
          </p>
          {!showWinRate && (
            <p className="text-xs text-[var(--text-muted)] mt-0.5">
              Win Rate after resolutions
            </p>
          )}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mt-4">
        <div className="h-4 w-full overflow-hidden rounded-full bg-[var(--bg-hover)]">
          <div
            className={`h-full transition-all duration-500 ${
              showWinRate
                ? meetsTarget ? 'bg-[var(--green)]' : 'bg-[var(--yellow)]'
                : 'bg-[var(--blue)]'
            }`}
            style={{ width: `${Math.min(100, displayRate)}%` }}
          />
        </div>
      </div>

      {/* Stats */}
      <div className="mt-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-2xl font-bold text-[var(--text-primary)]">
            {displayRate.toFixed(0)}%
          </span>
          {showWinRate && (
            <span className="text-sm text-[var(--text-secondary)]">
              {wins}W / {resolvedTrades} Total
            </span>
          )}
          {!showWinRate && (
            <span className="text-sm text-[var(--text-secondary)]">
              {resolvedTrades} resolved
            </span>
          )}
        </div>
        {showWinRate && (
          <span className={`text-sm ${meetsTarget ? 'text-[var(--green)]' : 'text-[var(--text-muted)]'}`}>
            Target: {targetWinRate}% {meetsTarget && '✓'}
          </span>
        )}
      </div>

      {/* Waiting message for early phase */}
      {!showWinRate && resolvedTrades < 10 && (
        <p className="mt-2 text-xs text-[var(--text-muted)]">
          Win rate available after {10 - resolvedTrades} more resolved trades
        </p>
      )}
    </div>
  );
}
