'use client';

import { AccountSnapshot } from '@/lib/supabase';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';

interface ExposureCardProps {
  account: AccountSnapshot | null;
}

export default function ExposureCard({ account }: ExposureCardProps) {
  const exposure = account?.total_exposure ?? 0;
  const balance = account?.balance ?? 2500;
  const available = balance - exposure;
  const exposurePct = balance > 0 ? (exposure / balance) * 100 : 0;

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const data = [
    { name: 'Deployed', value: exposure },
    { name: 'Available', value: available },
  ];

  const COLORS = ['var(--blue)', 'var(--bg-hover)'];

  return (
    <div className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] p-5">
      <p className="text-sm text-[var(--text-secondary)] uppercase tracking-wide">Exposure</p>

      <div className="mt-2 flex items-center gap-4">
        {/* Donut Chart */}
        <div className="relative h-24 w-24">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={28}
                outerRadius={40}
                paddingAngle={2}
                dataKey="value"
                startAngle={90}
                endAngle={-270}
                isAnimationActive={false}
              >
                {data.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
          {/* Center percentage */}
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-lg font-bold text-[var(--text-primary)]">
              {exposurePct.toFixed(0)}%
            </span>
          </div>
        </div>

        {/* Labels */}
        <div className="flex-1">
          <div className="flex items-center justify-between">
            <span className="text-sm text-[var(--text-secondary)]">Deployed</span>
            <span className="text-sm font-medium text-[var(--text-primary)]">{formatCurrency(exposure)}</span>
          </div>
          <div className="flex items-center justify-between mt-2">
            <span className="text-sm text-[var(--text-secondary)]">Available</span>
            <span className="text-sm font-medium text-[var(--text-primary)]">{formatCurrency(available)}</span>
          </div>
          <div className="flex items-center justify-between mt-2 pt-2 border-t border-[var(--border)]">
            <span className="text-sm text-[var(--text-secondary)]">Total</span>
            <span className="text-sm font-medium text-[var(--text-primary)]">{formatCurrency(balance)}</span>
          </div>
        </div>
      </div>
    </div>
  );
}
