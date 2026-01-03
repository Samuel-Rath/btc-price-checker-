import requests
import time
import json
import matplotlib.pyplot as plt
from datetime import datetime

# Function to fetch BTC data from CoinGecko API
def fetch_btc_data():
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
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
        print(f"Error fetching data: {e}")
        return None

# Main function to track BTC price and key factors, and plot charts
def track_btc(interval_seconds=60, iterations=10):
    timestamps = []
    prices = []
    market_caps = []
    volumes_24h = []
    changes_24h = []
    circulating_supplies = []
    total_supplies = []

    for i in range(iterations):
        data = fetch_btc_data()
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
        fig.suptitle('BTC Key Metrics Over Time')

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

        # 24h Change
        axs[1, 1].plot(timestamps, changes_24h, marker='o', color='red')
        axs[1, 1].set_title('24h Price Change (%)')
        axs[1, 1].set_ylabel('Change (%)')
        axs[1, 1].tick_params(axis='x', rotation=45)

        # Circulating Supply
        axs[2, 0].plot(timestamps, circulating_supplies, marker='o', color='purple')
        axs[2, 0].set_title('Circulating Supply')
        axs[2, 0].set_ylabel('Supply')
        axs[2, 0].tick_params(axis='x', rotation=45)

        # Total Supply
        axs[2, 1].plot(timestamps, total_supplies, marker='o', color='brown')
        axs[2, 1].set_title('Total Supply')
        axs[2, 1].set_ylabel('Supply')
        axs[2, 1].tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.show()

# Example usage: Track every 60 seconds for 10 iterations and plot at the end
if __name__ == "__main__":
    track_btc()