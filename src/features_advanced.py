import pandas as pd
import numpy as np

def add_advanced_features(df):
    """Add advanced technical indicators and features"""
    df = df.copy()
    
    # Basic features
    df['Daily_Return'] = df['Close'].pct_change()
    df['SMA20'] = df['Close'].rolling(window=20).mean()
    df['SMA50'] = df['Close'].rolling(window=50).mean()
    df['SMA200'] = df['Close'].rolling(window=200).mean()
    
    # RSI
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
    df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
    
    # Bollinger Bands
    df['BB_Middle'] = df['Close'].rolling(window=20).mean()
    bb_std = df['Close'].rolling(window=20).std()
    df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
    df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
    df['BB_Width'] = (df['BB_Upper'] - df['BB_Lower']) / df['BB_Middle']
    df['BB_Position'] = (df['Close'] - df['BB_Lower']) / (df['BB_Upper'] - df['BB_Lower'])
    
    # ATR (Average True Range) - Volatility
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    df['ATR'] = true_range.rolling(14).mean()
    
    # Volume indicators
    df['Volume_Change'] = df['Volume'].pct_change()
    df['Volume_SMA20'] = df['Volume'].rolling(window=20).mean()
    df['Volume_Ratio'] = df['Volume'] / df['Volume_SMA20']
    
    # Price momentum
    df['Momentum_5'] = df['Close'].pct_change(5)
    df['Momentum_10'] = df['Close'].pct_change(10)
    df['Momentum_20'] = df['Close'].pct_change(20)
    
    # Trend strength
    df['Trend_Strength'] = (df['Close'] - df['SMA50']) / df['SMA50']
    
    # Price position relative to high/low
    df['High_Low_Ratio'] = (df['Close'] - df['Low']) / (df['High'] - df['Low'])
    
    # Stochastic Oscillator
    low_14 = df['Low'].rolling(window=14).min()
    high_14 = df['High'].rolling(window=14).max()
    df['Stochastic'] = 100 * (df['Close'] - low_14) / (high_14 - low_14)
    
    # Rate of Change
    df['ROC'] = ((df['Close'] - df['Close'].shift(10)) / df['Close'].shift(10)) * 100
    
    # Target
    df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
    
    return df

def prepare_advanced_features(df):
    """Prepare advanced features for modeling"""
    df = add_advanced_features(df)
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()
    
    feature_cols = [
        'Close', 'Volume', 'Daily_Return', 
        'SMA20', 'SMA50', 'SMA200',
        'RSI', 'MACD', 'MACD_Signal', 'MACD_Hist',
        'BB_Width', 'BB_Position', 'ATR',
        'Volume_Change', 'Volume_Ratio',
        'Momentum_5', 'Momentum_10', 'Momentum_20',
        'Trend_Strength', 'High_Low_Ratio',
        'Stochastic', 'ROC'
    ]
    
    return df, feature_cols
