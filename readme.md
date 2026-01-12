# BTC Tracker Script README

## Overview

This Python script fetches real-time Bitcoin (BTC) price and key metrics from the CoinGecko API, tracks them over a specified number of iterations at regular intervals, prints the data to the console, and generates visualizations using Matplotlib. It collects data on:

- Current price (USD)
- Market capitalization (USD)
- 24-hour trading volume (USD)
- 24-hour price change (%)
- Circulating supply
- Total supply
- Prediction based on historical data

The script then plots these metrics in a 3x2 grid of line charts for easy trend analysis.

## Features

- Periodic data fetching with customizable interval and iterations.
- Console output of fetched data in JSON format.
- Visualizations of all key metrics over time using Matplotlib.
- Uses a free, public API (CoinGecko) – no API key required.
- Handles errors gracefully (e.g., network issues).
- Price comparison compared to other altcoins.

## Requirements

- Python 3.x
- Required libraries:
  - `requests` (for API calls)
  - `matplotlib` (for charting)
  - `datetime` and `time` (standard library, no installation needed)

Install dependencies via pip:
```
pip install requests matplotlib
```

## Usage

1. Save the script to a file, e.g., `btc_tracker.py`.

2. Run the script from the command line:
   ```
   python btc_tracker.py
   ```

3. The script will:
   - Fetch data every 60 seconds (default) for 10 iterations (default).
   - Print each fetch's data to the console.
   - After all iterations, display a Matplotlib window with charts.

4. Customization:
   - Modify the `track_btc()` call in the script to change parameters:
     ```python
     track_btc(interval_seconds=300, iterations=5)  # Example: Every 5 minutes, 5 times
     ```
   - Adjust the API URL or add more metrics if needed by extending `fetch_btc_data()`.

## Code Structure

- `fetch_btc_data()`: Fetches BTC data from CoinGecko API and returns a dictionary of key metrics.
- `track_btc(interval_seconds=60, iterations=10)`: Main function that loops to fetch data, stores it, prints it, and plots charts at the end.
- Charts are created using Matplotlib's subplots for each metric, with timestamps on the x-axis.

## Example Output

Console output for each iteration:
```
Iteration 1 at 2026-01-04 12:00:00:
{
    "price": 12345.67,
    "market_cap": 234567890123,
    "24h_volume": 34567890123,
    "24h_change": 1.23,
    "circulating_supply": 18901234.56,
    "total_supply": 21000000.0
}
```

After completion, a plot window appears with trends for all metrics.

## Disclaimer it might take a while for the plot to load

## Limitations

- Relies on CoinGecko API availability and rate limits (typically 50 calls/minute).
- Data is real-time but fetched at script runtime; for historical data, modify to use CoinGecko's historical endpoints.
- Charts are displayed in a blocking Matplotlib window; to save as files, add `plt.savefig('btc_charts.png')`.
- No persistent storage; data is in-memory only.

## Troubleshooting

- **API Errors**: Check internet connection or CoinGecko status. Rate limits may cause temporary failures.
- **Matplotlib Issues**: Ensure a graphical backend is available (e.g., not running in a headless environment).
- **Customization Errors**: Validate parameter types (e.g., `interval_seconds` as int).

## License

This script is provided as-is for educational purposes. Feel free to modify and use it under the MIT License.