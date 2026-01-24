'use client';

import { useEffect, useState } from 'react';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

interface CityForecast {
  id: number;
  city: string;
  target_date: string;
  peak_temp_low: number;
  peak_temp_high: number;
  peak_probability: number;
  percentile_10: number | null;
  percentile_50: number | null;
  percentile_90: number | null;
  updated_at: string;
}

function formatTemp(temp: number | null): string {
  if (temp === null) return '-';
  return `${Math.round(temp)}°F`;
}

function formatProb(prob: number | null): string {
  if (prob === null) return '-';
  return `${(prob * 100).toFixed(0)}%`;
}

function formatTime(timestamp: string): string {
  const date = new Date(timestamp);
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
}

export default function CityForecasts() {
  const [forecasts, setForecasts] = useState<CityForecast[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Initial fetch
    fetchForecasts();

    // Subscribe to realtime updates
    const channel = supabase
      .channel('city_forecasts_changes')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'city_forecasts' },
        () => {
          fetchForecasts();
        }
      )
      .subscribe();

    return () => {
      supabase.removeChannel(channel);
    };
  }, []);

  async function fetchForecasts() {
    const { data, error } = await supabase
      .from('city_forecasts')
      .select('*')
      .order('city', { ascending: true });

    if (error) {
      console.error('Error fetching forecasts:', error);
    } else {
      setForecasts(data || []);
    }
    setLoading(false);
  }

  if (loading) {
    return (
      <div className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] p-5">
        <p className="text-sm text-[var(--text-secondary)] uppercase tracking-wide mb-4">
          City Forecasts (NBM)
        </p>
        <div className="flex items-center justify-center h-32 text-[var(--text-muted)]">
          Loading...
        </div>
      </div>
    );
  }

  if (forecasts.length === 0) {
    return (
      <div className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] p-5">
        <p className="text-sm text-[var(--text-secondary)] uppercase tracking-wide mb-4">
          City Forecasts (NBM)
        </p>
        <div className="flex items-center justify-center h-32 text-[var(--text-muted)]">
          No forecast data yet. Run a scan to populate.
        </div>
      </div>
    );
  }

  // Get the target date from the first forecast
  const targetDate = forecasts[0]?.target_date;
  const formattedDate = targetDate
    ? new Date(targetDate + 'T12:00:00').toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })
    : 'Tomorrow';

  return (
    <div className="rounded-lg border border-[var(--border)] bg-[var(--bg-card)] p-5">
      <div className="flex justify-between items-center mb-4">
        <p className="text-sm text-[var(--text-secondary)] uppercase tracking-wide">
          City Forecasts - {formattedDate}
        </p>
        <p className="text-xs text-[var(--text-muted)]">
          NBM Model
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-[var(--border)]">
              <th className="text-left py-2 px-2 text-[var(--text-secondary)] font-medium">City</th>
              <th className="text-center py-2 px-2 text-[var(--text-secondary)] font-medium">Most Likely High</th>
              <th className="text-center py-2 px-2 text-[var(--text-secondary)] font-medium">Range (10-90%)</th>
              <th className="text-right py-2 px-2 text-[var(--text-secondary)] font-medium">Updated</th>
            </tr>
          </thead>
          <tbody>
            {forecasts.map((forecast) => (
              <tr key={forecast.id} className="border-b border-[var(--border)]/50 hover:bg-[var(--bg-hover)]">
                <td className="py-2 px-2 text-[var(--text-primary)] font-medium">
                  {forecast.city}
                </td>
                <td className="py-2 px-2 text-center">
                  <span className="text-[var(--text-primary)] font-bold">
                    {formatTemp(forecast.percentile_50)}
                  </span>
                  <span className="text-[var(--text-muted)] text-xs ml-1">
                    ({forecast.peak_temp_low}-{forecast.peak_temp_high}°F)
                  </span>
                </td>
                <td className="py-2 px-2 text-center text-[var(--text-secondary)]">
                  {formatTemp(forecast.percentile_10)} - {formatTemp(forecast.percentile_90)}
                </td>
                <td className="py-2 px-2 text-right text-[var(--text-muted)] text-xs">
                  {formatTime(forecast.updated_at)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
