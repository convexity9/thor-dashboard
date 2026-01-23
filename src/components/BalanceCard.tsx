'use client';

import { AccountSnapshot } from '@/lib/supabase';
import { AreaChart, Area, ResponsiveContainer, YAxis } from 'recharts';

interface BalanceCardProps {
  account: AccountSnapshot | null;
  balanceHistory: { timestamp: string; balance: number }[];
}

export default function BalanceCard({ account, balanceHistory }: BalanceCardProps) {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
    }).format(value);
  };

  const pnlToday = account?.pnl_today ?? 0;
  const isPositive = pnlToday >= 0;

  // Prepare sparkline data
  const sparklineData = balanceHistory.length > 0
    ? balanceHistory.map(h => ({ balance: h.balance }))
    : [{ balance: account?.balance ?? 2500 }];

  const minBalance = Math.min(...sparklineData.map(d => d.balance));
  const maxBalance = Math.max(...sparklineData.map(d => d.balance));
  const domain = minBalance === maxBalance
    ? [minBalance * 0.99, maxBalance * 1.01]
    : [minBalance * 0.995, maxBalance * 1.005];

  return (
    <div className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] p-5">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-[var(--text-secondary)] uppercase tracking-wide">Balance</p>
          <p className="text-3xl font-bold text-[var(--text-primary)] mt-1">
            {formatCurrency(account?.balance ?? 0)}
          </p>
          <p className={`text-sm mt-1 flex items-center gap-1 ${isPositive ? 'text-[var(--green)]' : 'text-[var(--red)]'}`}>
            <span>{isPositive ? '▲' : '▼'}</span>
            <span>{isPositive ? '+' : ''}{formatCurrency(pnlToday)} today</span>
          </p>
        </div>
      </div>

      {/* Sparkline */}
      <div className="mt-4 h-12">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={sparklineData}>
            <defs>
              <linearGradient id="balanceGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={isPositive ? 'var(--green)' : 'var(--red)'} stopOpacity={0.3} />
                <stop offset="95%" stopColor={isPositive ? 'var(--green)' : 'var(--red)'} stopOpacity={0} />
              </linearGradient>
            </defs>
            <YAxis domain={domain} hide />
            <Area
              type="monotone"
              dataKey="balance"
              stroke={isPositive ? 'var(--green)' : 'var(--red)'}
              strokeWidth={2}
              fill="url(#balanceGradient)"
              isAnimationActive={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
