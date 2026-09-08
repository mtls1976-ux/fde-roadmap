"""Day 6: fetch from an API, clean it with pandas, save a CSV.

Pulls a top-20-by-market-cap crypto snapshot from CoinGecko's free public
API (no key required) and saves a clean CSV.

Run:
    python day6_automation.py
"""
import requests
import pandas as pd

API_URL = "https://api.coingecko.com/api/v3/coins/markets"
OUTPUT_FILE = "day6_crypto_snapshot.csv"


def fetch_market_data(vs_currency="usd", top_n=20):
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": top_n,
        "page": 1,
    }
    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def clean(raw):
    df = pd.DataFrame(raw)

    # Keep only the columns worth keeping, renamed to something readable.
    keep = {
        "symbol": "symbol",
        "name": "name",
        "current_price": "price_usd",
        "market_cap": "market_cap_usd",
        "total_volume": "volume_24h_usd",
        "price_change_percentage_24h": "change_24h_pct",
    }
    df = df[list(keep.keys())].rename(columns=keep)

    df["symbol"] = df["symbol"].str.upper()

    # Missing values happen (a coin can have no 24h change reported yet) -
    # handle it explicitly instead of silently keeping NaN in the output.
    before = len(df)
    missing = df["change_24h_pct"].isna().sum()
    df["change_24h_pct"] = df["change_24h_pct"].fillna(0.0)
    print(f"Rows: {before} | filled {missing} missing 24h-change value(s) with 0.0")

    df["change_24h_pct"] = df["change_24h_pct"].round(2)
    df = df.sort_values("market_cap_usd", ascending=False).reset_index(drop=True)
    return df


if __name__ == "__main__":
    raw = fetch_market_data()
    df = clean(raw)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved {len(df)} rows to {OUTPUT_FILE}")
    print(df.head(10))
