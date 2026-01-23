'use client';

import { Trade } from '@/lib/supabase';
import { BarChart, Bar, XAxis, YAxis, ResponsiveContainer, Cell } from 'recharts';

interface ModelPerformanceProps {
  trades: Trade[];
}

interface ModelStats {
  name: string;
  accuracy: number;
  trades: number;
}

export default function ModelPerformance({ trades }: ModelPerformanceProps) {
  // Need at least 10 resolved trades to show meaningful data
  const minTrades = 10;

  if (trades.length < minTrades) {
    return (
      <div className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] p-5">
        <p className="text-sm text-[var(--text-secondary)] uppercase tracking-wide mb-4">
          Model Performance
        </p>
        <div className="flex items-center justify-center h-32 text-[var(--text-muted)]">
          Available after {minTrades - trades.length} more resolved trades
        </div>
      </div>
    );
  }

  // Calculate accuracy for each model
  const calculateModelAccuracy = (probKey: 'gfs_prob_at_entry' | 'ecmwf_prob_at_entry' | 'blended_prob_at_entry'): ModelStats => {
    const tradesWithModel = trades.filter(t => t[probKey] !== null);
    if (tradesWithModel.length === 0) {
      return { name: '', accuracy: 0, trades: 0 };
    }

    // A prediction is correct if:
    // - For BUY: model_prob > 0.5 and result is 'win' (contract settled YES)
    // - For SELL: model_prob < 0.5 and result is 'win' (contract settled NO)
    // But since we trade based on edge (model vs market), accuracy here means
    // the percentage of trades where the model's probability estimate led to profit
    const wins = tradesWithModel.filter(t => t.result === 'win').length;
    const accuracy = (wins / tradesWithModel.length) * 100;

    return {
      name: probKey.replace('_prob_at_entry', '').toUpperCase(),
      accuracy,
      trades: tradesWithModel.length,
    };
  };

  const gfsStats = calculateModelAccuracy('gfs_prob_at_entry');
  const ecmwfStats = calculateModelAccuracy('ecmwf_prob_at_entry');
  const blendedStats = calculateModelAccuracy('blended_prob_at_entry');

  const data: ModelStats[] = [
    { ...gfsStats, name: 'GFS' },
    { ...ecmwfStats, name: 'ECMWF' },
    { ...blendedStats, name: 'BLENDED' },
  ].filter(d => d.trades > 0);

  const getBarColor = (accuracy: number) => {
    if (accuracy >= 54) return 'var(--green)';
    if (accuracy >= 50) return 'var(--yellow)';
    return 'var(--red)';
  };

  return (
    <div className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] p-5">
      <p className="text-sm text-[var(--text-secondary)] uppercase tracking-wide mb-4">
        Model Performance
      </p>

      <div className="h-40">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <XAxis
              type="number"
              domain={[0, 100]}
              tick={{ fill: 'var(--text-muted)', fontSize: 12 }}
              axisLine={{ stroke: 'var(--border)' }}
              tickLine={false}
              tickFormatter={(v) => `${v}%`}
            />
            <YAxis
              type="category"
              dataKey="name"
              tick={{ fill: 'var(--text-secondary)', fontSize: 12 }}
              axisLine={false}
              tickLine={false}
              width={60}
            />
            <Bar dataKey="accuracy" radius={[0, 4, 4, 0]} isAnimationActive={false}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={getBarColor(entry.accuracy)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Legend */}
      <div className="mt-4 flex items-center justify-center gap-6 text-xs text-[var(--text-muted)]">
        {data.map((model) => (
          <div key={model.name} className="flex items-center gap-2">
            <span className="font-medium text-[var(--text-secondary)]">{model.name}</span>
            <span>{model.accuracy.toFixed(0)}%</span>
            <span>({model.trades} trades)</span>
          </div>
        ))}
      </div>
    </div>
  );
}
