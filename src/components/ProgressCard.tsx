'use client';

import { SystemStatus } from '@/lib/supabase';

interface ProgressCardProps {
  status: SystemStatus | null;
}

export default function ProgressCard({ status }: ProgressCardProps) {
  const count = status?.paper_trades_count ?? 0;
  const target = status?.paper_target ?? 50;
  const progress = (count / target) * 100;

  return (
    <div className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] p-5">
      <p className="text-sm text-[var(--text-secondary)] uppercase tracking-wide">Progress</p>

      {/* Progress Bar */}
      <div className="mt-4">
        <div className="h-4 w-full overflow-hidden rounded-full bg-[var(--bg-hover)]">
          <div
            className="h-full bg-[var(--blue)] transition-all duration-500"
            style={{ width: `${Math.min(100, progress)}%` }}
          />
        </div>
      </div>

      {/* Stats */}
      <div className="mt-3 flex items-center justify-between">
        <span className="text-2xl font-bold text-[var(--text-primary)]">
          {count}/{target}
        </span>
        <span className="text-sm text-[var(--text-secondary)]">
          Paper trades to validation
        </span>
      </div>

      {progress >= 100 && (
        <p className="mt-2 text-sm text-[var(--green)]">
          ✓ Ready for live validation
        </p>
      )}
    </div>
  );
}
