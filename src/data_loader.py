import yfinance as yf
import pandas as pd

def load_stock_data(ticker='RELIANCE.NS', period='5y'):
    """Load stock data from Yahoo Finance"""
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    df.reset_index(inplace=True)
    return df

def load_from_csv(filepath):
    """Load stock data from CSV file"""
    df = pd.read_csv(filepath)
    return df
