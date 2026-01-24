import { NextResponse } from 'next/server';
import { createClient, SupabaseClient } from '@supabase/supabase-js';
import * as crypto from 'crypto';

// Lazy-load Supabase client
let supabase: SupabaseClient | null = null;

function getSupabase(): SupabaseClient {
  if (!supabase) {
    const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
    // Use service key if available, otherwise fall back to anon key
    const key = process.env.SUPABASE_SERVICE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
    if (!url || !key) {
      throw new Error('Supabase credentials not configured');
    }
    supabase = createClient(url, key);
  }
  return supabase;
}

// Kalshi API configuration
const KALSHI_API_BASE = 'https://api.elections.kalshi.com/trade-api/v2';

interface Position {
  id: number;
  kalshi_ticker: string;
  direction: 'BUY' | 'SELL';
  current_price: number | null;
}

interface KalshiMarket {
  ticker: string;
  yes_bid: number;
  yes_ask: number;
  no_bid: number;
  no_ask: number;
}

/**
 * Sign a request for Kalshi API authentication
 */
function signRequest(
  privateKeyPem: string,
  timestamp: string,
  method: string,
  path: string
): string {
  const message = timestamp + method + path;
  const privateKey = crypto.createPrivateKey(privateKeyPem);
  const signature = crypto.sign('sha256', Buffer.from(message), {
    key: privateKey,
    padding: crypto.constants.RSA_PKCS1_PSS_PADDING,
    saltLength: crypto.constants.RSA_PSS_SALTLEN_DIGEST,
  });
  return signature.toString('base64');
}

/**
 * Fetch market data from Kalshi for a specific ticker
 */
async function fetchKalshiMarket(ticker: string): Promise<KalshiMarket | null> {
  const apiKey = process.env.KALSHI_API_KEY;
  const privateKey = process.env.KALSHI_PRIVATE_KEY;

  if (!apiKey || !privateKey) {
    console.error('Kalshi credentials not configured');
    return null;
  }

  try {
    const timestamp = Math.floor(Date.now() / 1000).toString();
    const method = 'GET';
    const path = `/trade-api/v2/markets/${ticker}`;

    // Format private key properly (replace literal \n with actual newlines)
    const formattedKey = privateKey.replace(/\\n/g, '\n');
    const signature = signRequest(formattedKey, timestamp, method, path);

    const response = await fetch(`${KALSHI_API_BASE}/markets/${ticker}`, {
      method: 'GET',
      headers: {
        'KALSHI-ACCESS-KEY': apiKey,
        'KALSHI-ACCESS-SIGNATURE': signature,
        'KALSHI-ACCESS-TIMESTAMP': timestamp,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      console.error(`Kalshi API error for ${ticker}: ${response.status}`);
      return null;
    }

    const data = await response.json();
    const market = data.market;

    return {
      ticker: market.ticker,
      yes_bid: (market.yes_bid || 0) / 100,
      yes_ask: (market.yes_ask || 0) / 100,
      no_bid: (market.no_bid || 0) / 100,
      no_ask: (market.no_ask || 0) / 100,
    };
  } catch (error) {
    console.error(`Error fetching market ${ticker}:`, error);
    return null;
  }
}

/**
 * Calculate mid price for a position based on direction
 */
function calculateCurrentPrice(market: KalshiMarket, direction: 'BUY' | 'SELL'): number {
  if (direction === 'BUY') {
    // BUY = holding YES contracts, use YES mid price
    return (market.yes_bid + market.yes_ask) / 2;
  } else {
    // SELL = holding NO contracts, use NO mid price
    return (market.no_bid + market.no_ask) / 2;
  }
}

export async function GET(request: Request) {
  // Optional: Add API key protection
  const authHeader = request.headers.get('authorization');
  const expectedKey = process.env.REFRESH_API_KEY;

  if (expectedKey && authHeader !== `Bearer ${expectedKey}`) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  try {
    // 1. Fetch open positions from Supabase
    const db = getSupabase();
    const { data: positions, error: fetchError } = await db
      .from('positions')
      .select('id, kalshi_ticker, direction, current_price')
      .eq('status', 'open');

    if (fetchError) {
      console.error('Error fetching positions:', fetchError);
      return NextResponse.json({ error: 'Failed to fetch positions' }, { status: 500 });
    }

    if (!positions || positions.length === 0) {
      return NextResponse.json({
        success: true,
        message: 'No open positions to update',
        updated: 0
      });
    }

    // 2. Fetch current prices from Kalshi and update
    let updated = 0;
    let failed = 0;
    const updates: { ticker: string; oldPrice: number | null; newPrice: number }[] = [];

    for (const position of positions as Position[]) {
      const market = await fetchKalshiMarket(position.kalshi_ticker);

      if (!market) {
        failed++;
        continue;
      }

      const newPrice = calculateCurrentPrice(market, position.direction);

      // 3. Update Supabase
      const { error: updateError } = await db
        .from('positions')
        .update({ current_price: newPrice })
        .eq('id', position.id);

      if (updateError) {
        console.error(`Error updating position ${position.id}:`, updateError);
        failed++;
      } else {
        updated++;
        updates.push({
          ticker: position.kalshi_ticker,
          oldPrice: position.current_price,
          newPrice: newPrice,
        });
      }

      // Small delay to avoid rate limiting
      await new Promise(resolve => setTimeout(resolve, 100));
    }

    return NextResponse.json({
      success: true,
      message: `Updated ${updated} positions`,
      updated,
      failed,
      updates,
      timestamp: new Date().toISOString(),
    });

  } catch (error) {
    console.error('Price refresh error:', error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}

// Also support POST for Vercel Cron
export async function POST(request: Request) {
  return GET(request);
}
