import requests
import time
import json

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

# Main function to track BTC price and key factors
def track_btc(interval_seconds=60, iterations=10):
    for i in range(iterations):
        data = fetch_btc_data()
        if data:
            print(f"Iteration {i+1}:")
            print(json.dumps(data, indent=4))
        else:
            print(f"Iteration {i+1}: Failed to fetch data.")
        time.sleep(interval_seconds)

# Example usage: Track every 60 seconds for 10 iterations
if __name__ == "__main__":
    track_btc()