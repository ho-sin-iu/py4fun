import yfinance as yf
import mplfinance as mpf
import pandas as pd
import sys
import argparse

def fetch_stock_data(ticker, period="1y", interval="1d"):
    """
    Fetch stock data for a given ticker.
    :param ticker: Stock ticker, e.g., "2330.TW"
    :param period: Time period, default is 1 year
    :param interval: Data interval, default is 1 day
    :return: DataFrame of stock data
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period=period, interval=interval)
    return data

def add_moving_averages(data):
    """
    Calculate and add moving averages (MA).
    :param data: DataFrame of stock data
    :return: DataFrame with added MAs
    """
    data['5d'] = data['Close'].rolling(window=5).mean()     # Weekly MA
    data['20d'] = data['Close'].rolling(window=20).mean()   # Monthly MA
    data['60d'] = data['Close'].rolling(window=60).mean()   # Quarterly MA
    data['240d'] = data['Close'].rolling(window=240).mean() # Yearly MA
    return data

def plot_stock_with_ma(data, ticker):
    """
    Plot candlestick chart with moving averages.
    :param data: DataFrame of stock data
    :param ticker: Stock ticker
    """
    add_plots = [
        mpf.make_addplot(data['5d'], color='red', label='5-day MA'),
        mpf.make_addplot(data['20d'], color='blue', label='20-day MA'),
        #mpf.make_addplot(data['60d'], color='green', label='60-day MA'),
        #mpf.make_addplot(data['240d'], color='purple', label='240-day MA')
    ]
    
    mpf.plot(data, type='candle', style='charles', 
             title=f"{ticker} Candlestick Chart with Moving Averages",
             ylabel='Price (NTD)',
             addplot=add_plots,
             volume=True)
  
def parse():
    parser = argparse.ArgumentParser(description='Plot candelstick charts with mplfinance and yfinance.')
    parser.add_argument('ticker', type=str, help='ticker (stock symbol)')
    parser.add_argument('--period', type=str, default='1y', help='data period, default = 1y')
    parser.add_argument('--interval', type=str, default='1d', help='data interval, default = 1d')
    
    args = parser.parse_args()
    
    ticker = args.ticker
    period = args.period
    interval = args.interval
    
    print(f'Ticker: {ticker}, period: {period}, interval: {interval}')
    return ticker, period, interval

if __name__ == '__main__':
    parsed = parse()
    data = fetch_stock_data(*parsed)
    data = add_moving_averages(data)
    plot_stock_with_ma(data, parsed[0])