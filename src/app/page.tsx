'use client';

import { useEffect, useState } from 'react';
import { supabase, AccountSnapshot, SystemStatus, Signal, Position } from '@/lib/supabase';
import StatusCard from '@/components/StatusCard';
import AccountCard from '@/components/AccountCard';
import SignalsTable from '@/components/SignalsTable';
import PositionsTable from '@/components/PositionsTable';

export default function Dashboard() {
  const [account, setAccount] = useState<AccountSnapshot | null>(null);
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [signals, setSignals] = useState<Signal[]>([]);
  const [positions, setPositions] = useState<Position[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      // Fetch latest account snapshot
      const { data: accountData, error: accountError } = await supabase
        .from('account_snapshots')
        .select('*')
        .order('timestamp', { ascending: false })
        .limit(1)
        .single();

      if (accountError && accountError.code !== 'PGRST116') throw accountError;
      setAccount(accountData);

      // Fetch system status
      const { data: statusData, error: statusError } = await supabase
        .from('system_status')
        .select('*')
        .eq('id', 1)
        .single();

      if (statusError && statusError.code !== 'PGRST116') throw statusError;
      setStatus(statusData);

      // Fetch recent signals (tradeable only, last 20)
      const { data: signalsData, error: signalsError } = await supabase
        .from('signals')
        .select('*')
        .in('action', ['BUY', 'SELL'])
        .order('timestamp', { ascending: false })
        .limit(20);

      if (signalsError) throw signalsError;
      setSignals(signalsData || []);

      // Fetch open positions
      const { data: positionsData, error: positionsError } = await supabase
        .from('positions')
        .select('*')
        .eq('status', 'open')
        .order('opened_at', { ascending: false });

      if (positionsError) throw positionsError;
      setPositions(positionsData || []);

      setError(null);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to fetch data from Supabase');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();

    // Set up real-time subscriptions
    const accountChannel = supabase
      .channel('account_changes')
      .on(
        'postgres_changes',
        { event: 'INSERT', schema: 'public', table: 'account_snapshots' },
        (payload) => {
          setAccount(payload.new as AccountSnapshot);
        }
      )
      .subscribe();

    const statusChannel = supabase
      .channel('status_changes')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'system_status' },
        (payload) => {
          setStatus(payload.new as SystemStatus);
        }
      )
      .subscribe();

    const signalsChannel = supabase
      .channel('signals_changes')
      .on(
        'postgres_changes',
        { event: 'INSERT', schema: 'public', table: 'signals' },
        () => {
          // Refetch signals to get properly ordered list
          fetchData();
        }
      )
      .subscribe();

    const positionsChannel = supabase
      .channel('positions_changes')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'positions' },
        () => {
          // Refetch positions
          fetchData();
        }
      )
      .subscribe();

    // Cleanup on unmount
    return () => {
      supabase.removeChannel(accountChannel);
      supabase.removeChannel(statusChannel);
      supabase.removeChannel(signalsChannel);
      supabase.removeChannel(positionsChannel);
    };
  }, []);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-zinc-950">
        <div className="text-center">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent mx-auto" />
          <p className="mt-4 text-zinc-600 dark:text-zinc-400">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950">
      <header className="border-b border-zinc-200 bg-white px-6 py-4 dark:border-zinc-800 dark:bg-zinc-900">
        <div className="mx-auto max-w-7xl flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-zinc-900 dark:text-zinc-100">Thor Dashboard</h1>
            <p className="text-sm text-zinc-500 dark:text-zinc-400">Algorithmic Prediction Market Trading</p>
          </div>
          <button
            onClick={fetchData}
            className="rounded-lg bg-zinc-100 px-4 py-2 text-sm font-medium text-zinc-700 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-zinc-300 dark:hover:bg-zinc-700"
          >
            Refresh
          </button>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-6 py-8">
        {error && (
          <div className="mb-6 rounded-lg bg-red-100 p-4 text-red-800 dark:bg-red-900/30 dark:text-red-200">
            {error}
          </div>
        )}

        <div className="grid gap-6 lg:grid-cols-2">
          <AccountCard account={account} />
          <StatusCard status={status} />
        </div>

        <div className="mt-6">
          <PositionsTable positions={positions} />
        </div>

        <div className="mt-6">
          <SignalsTable signals={signals} />
        </div>
      </main>

      <footer className="border-t border-zinc-200 bg-white px-6 py-4 dark:border-zinc-800 dark:bg-zinc-900">
        <div className="mx-auto max-w-7xl text-center text-sm text-zinc-500 dark:text-zinc-400">
          Thor v1.1 - Weather Prediction Market Trading System
        </div>
      </footer>
    </div>
  );
}
