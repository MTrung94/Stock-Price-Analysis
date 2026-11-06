import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def analyze_stocks():
    # Define tickers for at least two companies (e.g., Apple and Microsoft)
    tickers = ["AAPL", "MSFT"]
    
    print(f"Downloading historical stock data for {tickers}...")
    # Download historical stock data using yfinance (past 3 years)
    data = yf.download(tickers, period="3y", interval="1d")
    
    # Extract the 'Close' prices and 'Volume'
    # Depending on yfinance version, data might be multi-index. Let's handle 'Close'.
    if isinstance(data.columns, pd.MultiIndex):
        close_df = data['Close']
        volume_df = data['Volume']
    else:
        # Fallback structure if single ticker or different format
        close_df = data[['Close']]
        volume_df = data[['Volume']]

    print("\n--- Data Sample ---")
    print(close_df.head())

    # Ensure the index is set as DatetimeIndex (Date column as DataFrame index)
    close_df.index = pd.to_datetime(close_df.index)
    volume_df.index = pd.to_datetime(volume_df.index)

    # Plot closing prices over time using line charts
    plt.figure(figsize=(12, 6))
    for ticker in tickers:
        plt.plot(close_df.index, close_df[ticker], label=f"{ticker} Close Price")
    plt.title("Stock Closing Prices Over Time")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.legend()
    plt.grid(True)
    plt.savefig("charts/stock_closing_prices.png")
    plt.close()
    print("Saved closing prices chart to charts/stock_closing_prices.png")

    # Resample data to weekly and monthly frequency using .resample()
    print("\n--- Resampling Data ---")
    for ticker in tickers:
        print(f"\nWeekly Mean Closing Price for {ticker} (Last 5 weeks):")
        weekly_resampled = close_df[ticker].resample('W').mean()
        print(weekly_resampled.tail())

        print(f"\nMonthly Mean Closing Price for {ticker} (Last 5 months):")
        monthly_resampled = close_df[ticker].resample('M').mean()
        print(monthly_resampled.tail())

    # Compute 20-day and 200-day moving averages with .rolling()
    print("\n--- Computing Moving Averages ---")
    ma_dict = {}
    for ticker in tickers:
        ma_dict[f'{ticker}_MA20'] = close_df[ticker].rolling(window=20).mean()
        ma_dict[f'{ticker}_MA200'] = close_df[ticker].rolling(window=200).mean()
    
    ma_df = pd.DataFrame(ma_dict)
    print(ma_df.tail())

    # Compare trading volume between the two companies
    plt.figure(figsize=(12, 6))
    for ticker in tickers:
        plt.bar(volume_df.index, volume_df[ticker], label=f"{ticker} Volume", alpha=0.5)
    plt.title("Trading Volume Comparison")
    plt.xlabel("Date")
    plt.ylabel("Volume")
    plt.legend()
    plt.grid(True)
    plt.savefig("charts/trading_volume_comparison.png")
    plt.close()
    print("Saved volume comparison chart to charts/trading_volume_comparison.png")

if __name__ == "__main__":
    analyze_stocks()
