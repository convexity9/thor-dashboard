'use client';

import { AccountSnapshot } from '@/lib/supabase';

interface AccountCardProps {
  account: AccountSnapshot | null;
}

export default function AccountCard({ account }: AccountCardProps) {
  if (!account) {
    return (
      <div className="rounded-lg border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900">
        <h2 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Account Overview</h2>
        <p className="mt-2 text-zinc-500">Loading...</p>
      </div>
    );
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(value);
  };

  const formatPercent = (value: number) => {
    return `${(value * 100).toFixed(2)}%`;
  };

  return (
    <div className="rounded-lg border border-zinc-200 bg-white p-6 dark:border-zinc-800 dark:bg-zinc-900">
      <h2 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">Account Overview</h2>

      <div className="mt-4 grid grid-cols-2 gap-6">
        <div>
          <p className="text-sm text-zinc-500 dark:text-zinc-400">Balance</p>
          <p className="text-2xl font-bold text-zinc-900 dark:text-zinc-100">
            {formatCurrency(account.balance)}
          </p>
        </div>
        <div>
          <p className="text-sm text-zinc-500 dark:text-zinc-400">Deployed Capital</p>
          <p className="text-2xl font-bold text-zinc-900 dark:text-zinc-100">
            {formatCurrency(account.deployed)}
          </p>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-3 gap-4">
        <div className="rounded-lg bg-zinc-50 p-3 dark:bg-zinc-800">
          <p className="text-xs text-zinc-500 dark:text-zinc-400">P&L Today</p>
          <p className={`text-lg font-semibold ${
            account.pnl_today >= 0 ? 'text-green-600' : 'text-red-600'
          }`}>
            {account.pnl_today >= 0 ? '+' : ''}{formatCurrency(account.pnl_today)}
          </p>
        </div>
        <div className="rounded-lg bg-zinc-50 p-3 dark:bg-zinc-800">
          <p className="text-xs text-zinc-500 dark:text-zinc-400">Total P&L</p>
          <p className={`text-lg font-semibold ${
            account.pnl_total >= 0 ? 'text-green-600' : 'text-red-600'
          }`}>
            {account.pnl_total >= 0 ? '+' : ''}{formatCurrency(account.pnl_total)}
          </p>
        </div>
        <div className="rounded-lg bg-zinc-50 p-3 dark:bg-zinc-800">
          <p className="text-xs text-zinc-500 dark:text-zinc-400">Drawdown</p>
          <p className={`text-lg font-semibold ${
            account.drawdown_pct > 0.1 ? 'text-red-600' : 'text-zinc-900 dark:text-zinc-100'
          }`}>
            {formatPercent(account.drawdown_pct)}
          </p>
        </div>
      </div>

      <div className="mt-6 grid grid-cols-2 gap-4 border-t border-zinc-200 pt-4 dark:border-zinc-700">
        <div>
          <p className="text-sm text-zinc-500 dark:text-zinc-400">Open Positions</p>
          <p className="text-xl font-semibold text-zinc-900 dark:text-zinc-100">
            {account.open_positions}
          </p>
        </div>
        <div>
          <p className="text-sm text-zinc-500 dark:text-zinc-400">Total Exposure</p>
          <p className="text-xl font-semibold text-zinc-900 dark:text-zinc-100">
            {formatCurrency(account.total_exposure)}
          </p>
        </div>
      </div>
    </div>
  );
}
