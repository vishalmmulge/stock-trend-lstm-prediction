"""
Make predictions on new stock data using trained model
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow warnings

import numpy as np
from tensorflow.keras.models import load_model
from src.data_loader import load_stock_data
from src.features import prepare_features
from src.model import prepare_data
import argparse

def predict_next_day(ticker='RELIANCE.NS', model_path='stock_lstm_model.h5'):
    """Predict next day trend for a given stock"""
    
    print(f"\nLoading data for {ticker}...")
    df = load_stock_data(ticker, period='1y')
    
    print("Preparing features...")
    df, feature_cols = prepare_features(df)
    
    print("Loading model...")
    model = load_model(model_path)
    
    print("Preparing data...")
    X_train, X_test, y_train, y_test, scaler = prepare_data(df, feature_cols)
    
    # Get last sequence for prediction
    last_sequence = X_test[-1].reshape(1, X_test.shape[1], X_test.shape[2])
    
    # Make prediction
    prediction_prob = model.predict(last_sequence, verbose=0)[0][0]
    prediction_class = 1 if prediction_prob > 0.5 else 0
    
    # Get current price
    current_price = df.iloc[-1]['Close']
    current_date = df.iloc[-1]['Date']
    
    # Display results
    print("\n" + "="*60)
    print(f"PREDICTION FOR {ticker}")
    print("="*60)
    print(f"Current Date: {current_date.strftime('%Y-%m-%d')}")
    print(f"Current Close Price: ₹{current_price:.2f}")
    print(f"\nPrediction for Next Day:")
    print(f"  Trend: {'📈 UP' if prediction_class == 1 else '📉 DOWN'}")
    print(f"  Confidence: {prediction_prob*100:.2f}%")
    print(f"  Class: {prediction_class}")
    
    # Additional indicators
    print(f"\nCurrent Technical Indicators:")
    print(f"  RSI: {df.iloc[-1]['RSI']:.2f}")
    print(f"  SMA20: ₹{df.iloc[-1]['SMA20']:.2f}")
    print(f"  SMA50: ₹{df.iloc[-1]['SMA50']:.2f}")
    print(f"  MACD: {df.iloc[-1]['MACD']:.2f}")
    print("="*60)
    
    return {
        'ticker': ticker,
        'current_price': current_price,
        'prediction': prediction_class,
        'confidence': prediction_prob,
        'date': current_date
    }

def main():
    parser = argparse.ArgumentParser(description='Predict stock trend for next day')
    parser.add_argument('--ticker', type=str, default='RELIANCE.NS',
                        help='Stock ticker symbol (default: RELIANCE.NS)')
    parser.add_argument('--model', type=str, default='stock_lstm_model.h5',
                        help='Path to trained model (default: stock_lstm_model.h5)')
    
    args = parser.parse_args()
    
    try:
        predict_next_day(args.ticker, args.model)
    except FileNotFoundError:
        print("\n✗ Error: Model file not found!")
        print("Please train the model first by running: python -m src.train")
    except Exception as e:
        print(f"\n✗ Error: {e}")

if __name__ == '__main__':
    main()
