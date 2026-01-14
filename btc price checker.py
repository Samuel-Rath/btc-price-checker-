# Import required libraries 
import requests
import time
import json
import matplotlib.pyplot as plt
from datetime import datetime
import argparse  # Added for command-line argument parsing to streamline customization

# Function to fetch current BTC data from CoinGecko API
def fetch_current_btc_data():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data and isinstance(data, list):
            btc_data = data[0]
            return {
                "price": btc_data.get("current_price"),
                "market_cap": btc_data.get("market_cap"),
                "24h_volume": btc_data.get("total_volume"),
                "24h_change": btc_data.get("price_change_percentage_24h"),
                "circulating_supply": btc_data.get("circulating_supply"),
                "total_supply": btc_data.get("total_supply")
            }
        else:
            print("No data returned.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching current data: {e}")
        return None

# Function to fetch historical BTC data from CoinGecko API
def fetch_historical_btc_data(days=30):
    if days <= 0:
        return [], [], [], []
    url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days={days}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        timestamps = [datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d %H:%M:%S") for ts, _ in data.get("prices", [])]
        prices = [price for _, price in data.get("prices", [])]
        market_caps = [mc for _, mc in data.get("market_caps", [])]
        volumes_24h = [vol for _, vol in data.get("total_volumes", [])]
        return timestamps, prices, market_caps, volumes_24h
    except requests.exceptions.RequestException as e:
        print(f"Error fetching historical data: {e}")
        return [], [], [], []

# Main function to track BTC price and key factors, with optional historical data
def track_btc(interval_seconds=60, iterations=10, historical_days=30):
    # Fetch historical data
    hist_timestamps, hist_prices, hist_market_caps, hist_volumes_24h = fetch_historical_btc_data(historical_days)
    
    # Initialize lists with historical data (for plottable metrics)
    timestamps = hist_timestamps[:]
    prices = hist_prices[:]
    market_caps = hist_market_caps[:]
    volumes_24h = hist_volumes_24h[:]
    
    # Lists for metrics without historical data
    changes_24h = []
    circulating_supplies = []
    total_supplies = []

    # Real-time tracking loop
    for i in range(iterations):
        data = fetch_current_btc_data()
        if data:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            timestamps.append(now)
            prices.append(data["price"])
            market_caps.append(data["market_cap"])
            volumes_24h.append(data["24h_volume"])
            changes_24h.append(data["24h_change"])
            circulating_supplies.append(data["circulating_supply"])
            total_supplies.append(data["total_supply"])

            print(f"Iteration {i+1} at {now}:")
            print(json.dumps(data, indent=4))
        else:
            print(f"Iteration {i+1}: Failed to fetch data.")
        time.sleep(interval_seconds)

    # Plot the charts if data was collected
    if timestamps:
        fig, axs = plt.subplots(3, 2, figsize=(12, 12))
        fig.suptitle('BTC Key Metrics Over Time (Including Historical Data)')

        # Price
        axs[0, 0].plot(timestamps, prices, marker='o')
        axs[0, 0].set_title('Price (USD)')
        axs[0, 0].set_ylabel('Price')
        axs[0, 0].tick_params(axis='x', rotation=45)

        # Market Cap
        axs[0, 1].plot(timestamps, market_caps, marker='o', color='orange')
        axs[0, 1].set_title('Market Cap (USD)')
        axs[0, 1].set_ylabel('Market Cap')
        axs[0, 1].tick_params(axis='x', rotation=45)

        # 24h Volume
        axs[1, 0].plot(timestamps, volumes_24h, marker='o', color='green')
        axs[1, 0].set_title('24h Volume (USD)')
        axs[1, 0].set_ylabel('Volume')
        axs[1, 0].tick_params(axis='x', rotation=45)

        # 24h Change (only real-time)
        real_time_timestamps = timestamps[-iterations:] if iterations > 0 else []
        axs[1, 1].plot(real_time_timestamps, changes_24h, marker='o', color='red')
        axs[1, 1].set_title('24h Price Change (%)')
        axs[1, 1].set_ylabel('Change (%)')
        axs[1, 1].tick_params(axis='x', rotation=45)

        # Circulating Supply (only real-time)
        axs[2, 0].plot(real_time_timestamps, circulating_supplies, marker='o', color='purple')
        axs[2, 0].set_title('Circulating Supply')
        axs[2, 0].set_ylabel('Supply')
        axs[2, 0].tick_params(axis='x', rotation=45)

        # Total Supply (only real-time)
        axs[2, 1].plot(real_time_timestamps, total_supplies, marker='o', color='brown')
        axs[2, 1].set_title('Total Supply')
        axs[2, 1].set_ylabel('Supply')
        axs[2, 1].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.show()

# Parse command-line arguments to streamline configuration without editing code
def parse_args():
    parser = argparse.ArgumentParser(description="Track Bitcoin metrics with historical and real-time data.")
    parser.add_argument("--interval", type=int, default=60, help="Interval in seconds between data fetches (default: 60)")
    parser.add_argument("--iterations", type=int, default=10, help="Number of real-time data fetches (default: 10)")
    parser.add_argument("--historical_days", type=int, default=30, help="Number of historical days to fetch (default: 30)")
    return parser.parse_args()

# Example usage: Parse args and track BTC
if __name__ == "__main__":
    args = parse_args()
    track_btc(
        interval_seconds=args.interval,
        iterations=args.iterations,
        historical_days=args.historical_days
    )