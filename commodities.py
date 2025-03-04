import yfinance as yf

# Define tickers
tickers = {
    "Gold": "GC=F",
    "Silver": "SI=F",
    "Palladium": "PA=F",
    "Platinum": "PL=F",
    "Natural Gas": "NG=F",
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Solana": "SOL-USD"
}

# Fetch and display prices
for name, ticker in tickers.items():
    asset = yf.Ticker(ticker)
    current_price = asset.info['regularMarketPrice']
    last_close = asset.info['previousClose']
    percent_change = ((current_price - last_close) / last_close) * 100
    
    print(f"{name}:")
    print(f"  Current Price: ${current_price:.2f}")
    print(f"  Last Close:   ${last_close:.2f}")
    print(f"  Change:       {percent_change:.2f}%\n")

# Fetch all openings and closing since DATE
df = yf.download('GC=F', '2020-03-23')
print(df)