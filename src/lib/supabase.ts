import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Types for our database tables
export interface AccountSnapshot {
  id: number;
  timestamp: string;
  balance: number;
  deployed: number;
  pnl_today: number;
  pnl_total: number;
  peak_balance: number;
  drawdown_pct: number;
  open_positions: number;
  total_exposure: number;
  mode: 'paper' | 'live';
}

export interface Position {
  id: number;
  kalshi_ticker: string;
  city: string;
  target_date: string;
  threshold_temp: string;
  direction: 'BUY' | 'SELL';
  contracts: number;
  entry_price: number;
  current_price: number | null;
  edge_at_entry: number;
  model_prob: number | null;
  unrealized_pnl: number;
  opened_at: string;
  status: 'open' | 'closed';
}

export interface Signal {
  id: number;
  timestamp: string;
  kalshi_ticker: string;
  city: string;
  target_date: string;
  threshold_temp: string;
  gfs_prob: number | null;
  ecmwf_prob: number | null;
  blended_prob: number;
  model_disagreement: number | null;
  market_price: number;
  bid: number | null;
  ask: number | null;
  spread: number | null;
  edge: number;
  position_size_pct: number | null;
  action: 'BUY' | 'SELL' | 'SKIP';
  skip_reason: string | null;
  fill_status: 'pending' | 'filled' | 'unfilled' | 'n/a' | null;
}

export interface Trade {
  id: number;
  kalshi_ticker: string;
  city: string;
  target_date: string;
  direction: 'BUY' | 'SELL';
  contracts: number;
  entry_price: number;
  exit_price: number;
  gross_pnl: number;
  fees: number;
  net_pnl: number;
  edge_at_entry: number;
  gfs_prob_at_entry: number | null;
  ecmwf_prob_at_entry: number | null;
  blended_prob_at_entry: number | null;
  model_disagreement_at_entry: number | null;
  opened_at: string;
  closed_at: string;
  result: 'win' | 'loss';
}

export interface SystemStatus {
  id: number;
  updated_at: string;
  kalshi_api_ok: boolean;
  openmeteo_api_ok: boolean;
  last_forecast_time: string | null;
  forecast_age_hours: number | null;
  last_scan_time: string | null;
  next_scan_time: string | null;
  mode: 'paper' | 'live';
  circuit_breaker_active: boolean;
  circuit_breaker_reason: string | null;
  paper_trades_count: number;
  paper_target: number;
  win_rate: number | null;
  fill_rate: number | null;
}
