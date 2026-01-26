'use client';

import { useEffect, useState } from 'react';
import { supabase, ForecastTracking as ForecastTrackingType } from '@/lib/supabase';

interface Stats {
  total: number;
  settled: number;
  modelCorrect: number;
  modelAccuracy: number | null;
  avgEdgeAtOpen: number | null;
  avgEdgeWhenCorrect: number | null;
  avgEdgeWhenWrong: number | null;
}

export default function ForecastTracking() {
  const [forecasts, setForecasts] = useState<ForecastTrackingType[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [view, setView] = useState<'summary' | 'table'>('summary');

  useEffect(() => {
    fetchData();

    // Subscribe to changes
    const channel = supabase
      .channel('forecast_tracking_changes')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'forecast_tracking' },
        () => {
          fetchData();
        }
      )
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

  const fetchData = async () => {
    try {
      const { data, error } = await supabase
        .from('forecast_tracking')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(100);

      if (error) throw error;
      setForecasts(data || []);

      // Calculate stats
      if (data && data.length > 0) {
        const settled = data.filter(f => f.settlement_result !== null);
        const correct = settled.filter(f => f.model_correct === true);
        const wrong = settled.filter(f => f.model_correct === false);

        const edgesAtOpen = data
          .filter(f => f.edge_at_open !== null)
          .map(f => f.edge_at_open as number);

        const edgesWhenCorrect = correct
          .filter(f => f.edge_at_open !== null)
          .map(f => f.edge_at_open as number);

        const edgesWhenWrong = wrong
          .filter(f => f.edge_at_open !== null)
          .map(f => f.edge_at_open as number);

        setStats({
          total: data.length,
          settled: settled.length,
          modelCorrect: correct.length,
          modelAccuracy: settled.length > 0 ? (correct.length / settled.length) * 100 : null,
          avgEdgeAtOpen: edgesAtOpen.length > 0
            ? edgesAtOpen.reduce((a, b) => a + b, 0) / edgesAtOpen.length
            : null,
          avgEdgeWhenCorrect: edgesWhenCorrect.length > 0
            ? edgesWhenCorrect.reduce((a, b) => a + b, 0) / edgesWhenCorrect.length
            : null,
          avgEdgeWhenWrong: edgesWhenWrong.length > 0
            ? edgesWhenWrong.reduce((a, b) => a + b, 0) / edgesWhenWrong.length
            : null,
        });
      }
    } catch (err) {
      console.error('Error fetching forecast tracking:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] p-5">
        <p className="text-sm text-[var(--text-secondary)] uppercase tracking-wide mb-4">
          Forecast Tracking
        </p>
        <div className="flex items-center justify-center h-32">
          <div className="h-6 w-6 animate-spin rounded-full border-2 border-[var(--blue)] border-t-transparent" />
        </div>
      </div>
    );
  }

  if (forecasts.length === 0) {
    return (
      <div className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] p-5">
        <p className="text-sm text-[var(--text-secondary)] uppercase tracking-wide mb-4">
          Forecast Tracking
        </p>
        <div className="flex items-center justify-center h-32 text-[var(--text-muted)]">
          No forecasts tracked yet. Data will appear after the next scan.
        </div>
      </div>
    );
  }

  const getAccuracyColor = (accuracy: number | null) => {
    if (accuracy === null) return 'var(--text-muted)';
    if (accuracy >= 55) return 'var(--green)';
    if (accuracy >= 50) return 'var(--yellow)';
    return 'var(--red)';
  };

  const formatEdge = (edge: number | null) => {
    if (edge === null) return '-';
    const sign = edge >= 0 ? '+' : '';
    return `${sign}${(edge * 100).toFixed(1)}%`;
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  // Group by settlement result for analysis
  const settledForecasts = forecasts.filter(f => f.settlement_result !== null);
  const pendingForecasts = forecasts.filter(f => f.settlement_result === null);

  return (
    <div className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] p-5">
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm text-[var(--text-secondary)] uppercase tracking-wide">
          Forecast Tracking (NBM vs Settlement)
        </p>
        <div className="flex gap-2">
          <button
            onClick={() => setView('summary')}
            className={`px-3 py-1 text-xs rounded ${
              view === 'summary'
                ? 'bg-[var(--blue)] text-white'
                : 'bg-[var(--bg-hover)] text-[var(--text-secondary)]'
            }`}
          >
            Summary
          </button>
          <button
            onClick={() => setView('table')}
            className={`px-3 py-1 text-xs rounded ${
              view === 'table'
                ? 'bg-[var(--blue)] text-white'
                : 'bg-[var(--bg-hover)] text-[var(--text-secondary)]'
            }`}
          >
            Details
          </button>
        </div>
      </div>

      {view === 'summary' && stats && (
        <div className="space-y-4">
          {/* Key Metrics */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-[var(--bg-primary)] rounded-lg p-3">
              <p className="text-xs text-[var(--text-muted)] mb-1">Tracked</p>
              <p className="text-xl font-bold text-[var(--text-primary)]">{stats.total}</p>
            </div>
            <div className="bg-[var(--bg-primary)] rounded-lg p-3">
              <p className="text-xs text-[var(--text-muted)] mb-1">Settled</p>
              <p className="text-xl font-bold text-[var(--text-primary)]">{stats.settled}</p>
            </div>
            <div className="bg-[var(--bg-primary)] rounded-lg p-3">
              <p className="text-xs text-[var(--text-muted)] mb-1">Model Accuracy</p>
              <p
                className="text-xl font-bold"
                style={{ color: getAccuracyColor(stats.modelAccuracy) }}
              >
                {stats.modelAccuracy !== null ? `${stats.modelAccuracy.toFixed(1)}%` : '-'}
              </p>
            </div>
            <div className="bg-[var(--bg-primary)] rounded-lg p-3">
              <p className="text-xs text-[var(--text-muted)] mb-1">Avg Edge @ Open</p>
              <p className="text-xl font-bold text-[var(--text-primary)]">
                {formatEdge(stats.avgEdgeAtOpen)}
              </p>
            </div>
          </div>

          {/* Edge Analysis */}
          {stats.settled > 0 && (
            <div className="bg-[var(--bg-primary)] rounded-lg p-4">
              <p className="text-xs text-[var(--text-muted)] mb-3 uppercase">Edge Analysis</p>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-xs text-[var(--text-muted)]">Avg Edge (Correct Predictions)</p>
                  <p className="text-lg font-semibold text-[var(--green)]">
                    {formatEdge(stats.avgEdgeWhenCorrect)}
                  </p>
                  <p className="text-xs text-[var(--text-muted)]">{stats.modelCorrect} trades</p>
                </div>
                <div>
                  <p className="text-xs text-[var(--text-muted)]">Avg Edge (Wrong Predictions)</p>
                  <p className="text-lg font-semibold text-[var(--red)]">
                    {formatEdge(stats.avgEdgeWhenWrong)}
                  </p>
                  <p className="text-xs text-[var(--text-muted)]">{stats.settled - stats.modelCorrect} trades</p>
                </div>
              </div>
            </div>
          )}

          {/* Pending Forecasts */}
          {pendingForecasts.length > 0 && (
            <div className="bg-[var(--bg-primary)] rounded-lg p-4">
              <p className="text-xs text-[var(--text-muted)] mb-2 uppercase">
                Pending Settlement ({pendingForecasts.length})
              </p>
              <div className="space-y-2 max-h-32 overflow-y-auto">
                {pendingForecasts.slice(0, 5).map((f) => (
                  <div key={f.id} className="flex justify-between text-sm">
                    <span className="text-[var(--text-secondary)]">
                      {f.city} {f.threshold_temp} ({formatDate(f.target_date)})
                    </span>
                    <span className="text-[var(--text-muted)]">
                      NBM: {f.nbm_mean?.toFixed(0)}F | Model: {((f.model_probability || 0) * 100).toFixed(0)}%
                    </span>
                  </div>
                ))}
                {pendingForecasts.length > 5 && (
                  <p className="text-xs text-[var(--text-muted)]">
                    +{pendingForecasts.length - 5} more...
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
      )}

      {view === 'table' && (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs text-[var(--text-muted)] uppercase">
                <th className="pb-2">Contract</th>
                <th className="pb-2">NBM</th>
                <th className="pb-2">Model %</th>
                <th className="pb-2">Market</th>
                <th className="pb-2">Edge</th>
                <th className="pb-2">Result</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--border)]">
              {forecasts.slice(0, 20).map((f) => (
                <tr key={f.id} className="text-[var(--text-secondary)]">
                  <td className="py-2">
                    <div className="font-medium text-[var(--text-primary)]">{f.city}</div>
                    <div className="text-xs text-[var(--text-muted)]">
                      {f.threshold_temp} | {formatDate(f.target_date)}
                    </div>
                  </td>
                  <td className="py-2">
                    {f.nbm_mean !== null ? `${f.nbm_mean.toFixed(0)}F` : '-'}
                    {f.nbm_std !== null && (
                      <span className="text-xs text-[var(--text-muted)]"> ±{f.nbm_std.toFixed(1)}</span>
                    )}
                  </td>
                  <td className="py-2">
                    {f.model_probability !== null ? `${(f.model_probability * 100).toFixed(0)}%` : '-'}
                  </td>
                  <td className="py-2">
                    {f.market_price_open !== null ? `$${f.market_price_open.toFixed(2)}` : '-'}
                  </td>
                  <td className="py-2">
                    <span className={f.edge_at_open && f.edge_at_open > 0 ? 'text-[var(--green)]' : 'text-[var(--red)]'}>
                      {formatEdge(f.edge_at_open)}
                    </span>
                  </td>
                  <td className="py-2">
                    {f.settlement_result === null ? (
                      <span className="text-[var(--text-muted)]">Pending</span>
                    ) : (
                      <span className={f.model_correct ? 'text-[var(--green)]' : 'text-[var(--red)]'}>
                        {f.settlement_result.toUpperCase()}
                        {f.model_correct !== null && (
                          <span className="ml-1">{f.model_correct ? '✓' : '✗'}</span>
                        )}
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {forecasts.length > 20 && (
            <p className="text-center text-xs text-[var(--text-muted)] mt-2">
              Showing 20 of {forecasts.length} tracked forecasts
            </p>
          )}
        </div>
      )}
    </div>
  );
}
