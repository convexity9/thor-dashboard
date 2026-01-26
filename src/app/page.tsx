'use client';

import { useEffect, useState } from 'react';
import { supabase, AccountSnapshot, SystemStatus, Signal, Position, Trade } from '@/lib/supabase';
import Header from '@/components/Header';
import BalanceCard from '@/components/BalanceCard';
import WinRateCard from '@/components/WinRateCard';
import ProgressCard from '@/components/ProgressCard';
import ExposureCard from '@/components/ExposureCard';
import PnLChart from '@/components/PnLChart';
import PositionsBars from '@/components/PositionsBars';
import SignalsBars from '@/components/SignalsBars';
import ModelPerformance from '@/components/ModelPerformance';
import CityForecasts from '@/components/CityForecasts';
import ForecastTracking from '@/components/ForecastTracking';

interface PnLDataPoint {
  timestamp: string;
  pnl_total: number;
  balance: number;
}

export default function Dashboard() {
  const [account, setAccount] = useState<AccountSnapshot | null>(null);
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [signals, setSignals] = useState<Signal[]>([]);
  const [positions, setPositions] = useState<Position[]>([]);
  const [trades, setTrades] = useState<Trade[]>([]);
  const [balanceHistory, setBalanceHistory] = useState<{ timestamp: string; balance: number }[]>([]);
  const [pnlHistory, setPnlHistory] = useState<PnLDataPoint[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
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

      // Fetch balance history for sparkline (last 30 days)
      const { data: historyData, error: historyError } = await supabase
        .from('account_snapshots')
        .select('timestamp, balance, pnl_total')
        .order('timestamp', { ascending: true })
        .limit(100);

      if (historyError) throw historyError;
      setBalanceHistory(historyData?.map(h => ({ timestamp: h.timestamp, balance: h.balance })) || []);
      setPnlHistory(historyData?.map(h => ({
        timestamp: h.timestamp,
        pnl_total: h.pnl_total,
        balance: h.balance,
      })) || []);

      // Fetch system status
      const { data: statusData, error: statusError } = await supabase
        .from('system_status')
        .select('*')
        .eq('id', 1)
        .single();

      if (statusError && statusError.code !== 'PGRST116') throw statusError;
      setStatus(statusData);

      // Fetch recent signals (tradeable only, last 50)
      const { data: signalsData, error: signalsError } = await supabase
        .from('signals')
        .select('*')
        .order('timestamp', { ascending: false })
        .limit(50);

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

      // Fetch all trades for model performance
      const { data: tradesData, error: tradesError } = await supabase
        .from('trades')
        .select('*')
        .order('closed_at', { ascending: false });

      if (tradesError) throw tradesError;
      setTrades(tradesData || []);

      setError(null);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to fetch data from Supabase');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchData();
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
          setBalanceHistory(prev => [...prev, {
            timestamp: (payload.new as AccountSnapshot).timestamp,
            balance: (payload.new as AccountSnapshot).balance,
          }]);
          setPnlHistory(prev => [...prev, {
            timestamp: (payload.new as AccountSnapshot).timestamp,
            pnl_total: (payload.new as AccountSnapshot).pnl_total,
            balance: (payload.new as AccountSnapshot).balance,
          }]);
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
          fetchData();
        }
      )
      .subscribe();

    const tradesChannel = supabase
      .channel('trades_changes')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'trades' },
        () => {
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
      supabase.removeChannel(tradesChannel);
    };
  }, []);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-[var(--bg-primary)]">
        <div className="text-center">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-[var(--blue)] border-t-transparent mx-auto" />
          <p className="mt-4 text-[var(--text-secondary)]">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  const hasResolvedTrades = trades.length > 0;

  return (
    <div className="min-h-screen bg-[var(--bg-primary)]">
      <Header status={status} onRefresh={handleRefresh} isRefreshing={refreshing} />

      <main className="mx-auto max-w-7xl px-6 py-6">
        {error && (
          <div className="mb-6 rounded-lg bg-[var(--red)]/20 border border-[var(--red)]/30 p-4 text-[var(--red)]">
            {error}
          </div>
        )}

        {/* Top Row: Balance, Win Rate */}
        <div className="grid gap-4 md:grid-cols-2">
          <BalanceCard account={account} balanceHistory={balanceHistory} />
          <WinRateCard status={status} trades={trades} />
        </div>

        {/* Second Row: Progress, Exposure */}
        <div className="mt-4 grid gap-4 md:grid-cols-2">
          <ProgressCard status={status} />
          <ExposureCard account={account} />
        </div>

        {/* P&L Chart */}
        <div className="mt-6">
          <PnLChart data={pnlHistory} hasResolvedTrades={hasResolvedTrades} />
        </div>

        {/* Positions and Signals */}
        <div className="mt-6 grid gap-4 md:grid-cols-2">
          <PositionsBars positions={positions} />
          <SignalsBars signals={signals} />
        </div>

        {/* City Forecasts */}
        <div className="mt-6">
          <CityForecasts />
        </div>

        {/* Model Performance */}
        <div className="mt-6">
          <ModelPerformance trades={trades} />
        </div>

        {/* Forecast Tracking - NBM vs Settlement Analysis */}
        <div className="mt-6">
          <ForecastTracking />
        </div>
      </main>

      <footer className="border-t border-[var(--border)] bg-[var(--bg-card)] px-6 py-4 mt-6">
        <div className="mx-auto max-w-7xl text-center text-sm text-[var(--text-muted)]">
          Thor v1.1 - Weather Prediction Market Trading System
        </div>
      </footer>
    </div>
  );
}
