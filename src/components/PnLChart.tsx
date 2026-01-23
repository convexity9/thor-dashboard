'use client';

import { useState } from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts';

interface PnLDataPoint {
  timestamp: string;
  pnl_total: number;
  balance: number;
}

interface PnLChartProps {
  data: PnLDataPoint[];
  hasResolvedTrades: boolean;
}

type TimeRange = '7D' | '30D' | 'ALL';

export default function PnLChart({ data, hasResolvedTrades }: PnLChartProps) {
  const [timeRange, setTimeRange] = useState<TimeRange>('7D');

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const formatDate = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  // Filter data based on time range
  const filterData = () => {
    if (data.length === 0) return [];

    const now = new Date();
    let cutoff: Date;

    switch (timeRange) {
      case '7D':
        cutoff = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
        break;
      case '30D':
        cutoff = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
        break;
      default:
        return data;
    }

    return data.filter(d => new Date(d.timestamp) >= cutoff);
  };

  const filteredData = filterData();

  // Calculate domain for better visualization
  const pnlValues = filteredData.map(d => d.pnl_total);
  const minPnl = pnlValues.length > 0 ? Math.min(...pnlValues, 0) : -100;
  const maxPnl = pnlValues.length > 0 ? Math.max(...pnlValues, 0) : 100;
  const padding = Math.max(Math.abs(maxPnl - minPnl) * 0.1, 10);

  // Custom tooltip
  const CustomTooltip = ({ active, payload }: { active?: boolean; payload?: Array<{ payload: PnLDataPoint }> }) => {
    if (active && payload && payload.length) {
      const d = payload[0].payload;
      return (
        <div className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] p-3 shadow-lg">
          <p className="text-sm text-[var(--text-secondary)]">{formatDate(d.timestamp)}</p>
          <p className={`text-lg font-bold ${d.pnl_total >= 0 ? 'text-[var(--green)]' : 'text-[var(--red)]'}`}>
            {d.pnl_total >= 0 ? '+' : ''}{formatCurrency(d.pnl_total)}
          </p>
          <p className="text-sm text-[var(--text-muted)]">Balance: {formatCurrency(d.balance)}</p>
        </div>
      );
    }
    return null;
  };

  // Empty state
  if (!hasResolvedTrades || filteredData.length === 0) {
    return (
      <div className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] p-5">
        <div className="flex items-center justify-between mb-4">
          <p className="text-sm text-[var(--text-secondary)] uppercase tracking-wide">P&L Over Time</p>
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value as TimeRange)}
            className="bg-[var(--bg-hover)] border border-[var(--border)] rounded px-2 py-1 text-sm text-[var(--text-secondary)]"
          >
            <option value="7D">7D</option>
            <option value="30D">30D</option>
            <option value="ALL">All</option>
          </select>
        </div>

        <div className="h-64 flex flex-col items-center justify-center">
          <div className="w-full h-px bg-[var(--border)] mb-4" />
          <p className="text-[var(--text-muted)] text-center">
            P&L chart will populate as trades resolve
          </p>
          <p className="text-sm text-[var(--text-muted)] mt-2">
            Open positions will show unrealized P&L once the market has activity
          </p>
        </div>
      </div>
    );
  }

  const latestPnl = filteredData[filteredData.length - 1]?.pnl_total ?? 0;
  const isPositive = latestPnl >= 0;

  return (
    <div className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] p-5">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-4">
          <p className="text-sm text-[var(--text-secondary)] uppercase tracking-wide">P&L Over Time</p>
          <span className={`text-lg font-bold ${isPositive ? 'text-[var(--green)]' : 'text-[var(--red)]'}`}>
            {isPositive ? '+' : ''}{formatCurrency(latestPnl)}
          </span>
        </div>
        <select
          value={timeRange}
          onChange={(e) => setTimeRange(e.target.value as TimeRange)}
          className="bg-[var(--bg-hover)] border border-[var(--border)] rounded px-2 py-1 text-sm text-[var(--text-secondary)]"
        >
          <option value="7D">7D</option>
          <option value="30D">30D</option>
          <option value="ALL">All</option>
        </select>
      </div>

      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={filteredData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="pnlGradientPositive" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="var(--green)" stopOpacity={0.3} />
                <stop offset="95%" stopColor="var(--green)" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="pnlGradientNegative" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="var(--red)" stopOpacity={0.3} />
                <stop offset="95%" stopColor="var(--red)" stopOpacity={0} />
              </linearGradient>
            </defs>
            <XAxis
              dataKey="timestamp"
              tickFormatter={formatDate}
              tick={{ fill: 'var(--text-muted)', fontSize: 12 }}
              axisLine={{ stroke: 'var(--border)' }}
              tickLine={false}
            />
            <YAxis
              domain={[minPnl - padding, maxPnl + padding]}
              tickFormatter={(v) => `$${v}`}
              tick={{ fill: 'var(--text-muted)', fontSize: 12 }}
              axisLine={false}
              tickLine={false}
              width={50}
            />
            <Tooltip content={<CustomTooltip />} />
            <ReferenceLine y={0} stroke="var(--text-muted)" strokeDasharray="3 3" />
            <Area
              type="monotone"
              dataKey="pnl_total"
              stroke={isPositive ? 'var(--green)' : 'var(--red)'}
              strokeWidth={2}
              fill={isPositive ? 'url(#pnlGradientPositive)' : 'url(#pnlGradientNegative)'}
              isAnimationActive={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
