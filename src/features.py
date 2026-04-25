import pandas as pd
import numpy as np

def add_technical_indicators(df):
    """Add technical indicators to the dataframe"""
    df = df.copy()
    
    # Daily return
    df['Daily_Return'] = df['Close'].pct_change()
    
    # SMA 20 and 50
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    
    # RSI (14)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    exp1 = df['Close'].ewm(span=12, adjust=False).mean()
    exp2 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = exp1 - exp2
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    
    # Volume change %
    df['Volume_Change'] = df['Volume'].pct_change()
    
    # Target: 1 if next day close > today close, else 0
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
    
    return df

def prepare_features(df):
    """Select and prepare features for modeling"""
    df = add_technical_indicators(df)
    df = df.dropna()
    
    feature_cols = ['Close', 'Volume', 'Daily_Return', 'SMA20', 'SMA50', 
                    'RSI', 'MACD', 'MACD_Signal', 'Volume_Change']
    
    # Replace infinity values with NaN and drop them
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()
    
    return df, feature_cols
