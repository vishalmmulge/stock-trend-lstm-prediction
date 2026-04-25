import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from src.data_loader import load_stock_data
from src.features import prepare_features
from src.model import prepare_data
import argparse

def calculate_swing_signals(df):
    """Calculate swing trading signals"""
    signals = {}
    current = df.iloc[-1]
    
    # Trend Analysis
    if current['Close'] > current['SMA20'] > current['SMA50']:
        signals['trend'] = 'STRONG UPTREND'
        signals['trend_score'] = 3
    elif current['Close'] > current['SMA20']:
        signals['trend'] = 'UPTREND'
        signals['trend_score'] = 2
    elif current['Close'] < current['SMA20'] < current['SMA50']:
        signals['trend'] = 'STRONG DOWNTREND'
        signals['trend_score'] = -3
    else:
        signals['trend'] = 'DOWNTREND'
        signals['trend_score'] = -2
    
    # RSI Analysis
    rsi = current['RSI']
    if rsi < 30:
        signals['rsi_signal'] = 'OVERSOLD - BUY'
        signals['rsi_score'] = 3
    elif rsi < 40:
        signals['rsi_signal'] = 'NEAR OVERSOLD - WATCH'
        signals['rsi_score'] = 2
    elif rsi > 70:
        signals['rsi_signal'] = 'OVERBOUGHT - SELL'
        signals['rsi_score'] = -3
    elif rsi > 60:
        signals['rsi_signal'] = 'NEAR OVERBOUGHT - CAUTION'
        signals['rsi_score'] = -2
    else:
        signals['rsi_signal'] = 'NEUTRAL'
        signals['rsi_score'] = 0
    
    # MACD Analysis
    if current['MACD'] > current['MACD_Signal'] and current['MACD'] > 0:
        signals['macd_signal'] = 'BULLISH CROSSOVER'
        signals['macd_score'] = 3
    elif current['MACD'] > current['MACD_Signal']:
        signals['macd_signal'] = 'BULLISH'
        signals['macd_score'] = 2
    elif current['MACD'] < current['MACD_Signal'] and current['MACD'] < 0:
        signals['macd_signal'] = 'BEARISH CROSSOVER'
        signals['macd_score'] = -3
    else:
        signals['macd_signal'] = 'BEARISH'
        signals['macd_score'] = -2
    
    # Volume Analysis
    if current['Volume_Change'] > 0.5:
        signals['volume_signal'] = 'HIGH VOLUME SURGE'
        signals['volume_score'] = 2
    elif current['Volume_Change'] > 0.2:
        signals['volume_signal'] = 'ABOVE AVERAGE'
        signals['volume_score'] = 1
    else:
        signals['volume_signal'] = 'NORMAL'
        signals['volume_score'] = 0
    
    return signals

def generate_swing_recommendation(ticker='RELIANCE.NS', model_path='stock_lstm_model.h5'):
    """Generate swing trading recommendation"""
    
    print(f"\n{'='*70}")
    print(f"SWING TRADING RECOMMENDATION - {ticker}")
    print(f"{'='*70}\n")
    
    # Load data
    df = load_stock_data(ticker, period='1y')
    df, feature_cols = prepare_features(df)
    
    # Get current price info
    current = df.iloc[-1]
    prev = df.iloc[-2]
    
    print(f"📊 CURRENT MARKET DATA")
    print(f"{'─'*70}")
    print(f"Date: {current['Date'].strftime('%Y-%m-%d')}")
    print(f"Current Price: ₹{current['Close']:.2f}")
    print(f"Previous Close: ₹{prev['Close']:.2f}")
    print(f"Change: {((current['Close'] - prev['Close']) / prev['Close'] * 100):.2f}%")
    print(f"Volume: {current['Volume']:,.0f}")
    
    # Technical Indicators
    print(f"\n📈 TECHNICAL INDICATORS")
    print(f"{'─'*70}")
    print(f"RSI (14): {current['RSI']:.2f}")
    print(f"SMA20: ₹{current['SMA20']:.2f}")
    print(f"SMA50: ₹{current['SMA50']:.2f}")
    print(f"MACD: {current['MACD']:.2f}")
    print(f"MACD Signal: {current['MACD_Signal']:.2f}")
    
    # Calculate swing signals
    signals = calculate_swing_signals(df)
    
    print(f"\n🎯 SWING TRADING SIGNALS")
    print(f"{'─'*70}")
    print(f"Trend: {signals['trend']}")
    print(f"RSI Signal: {signals['rsi_signal']}")
    print(f"MACD Signal: {signals['macd_signal']}")
    print(f"Volume: {signals['volume_signal']}")
    
    # Calculate total score
    total_score = (signals['trend_score'] + signals['rsi_score'] + 
                   signals['macd_score'] + signals['volume_score'])
    
    # Load model for prediction
    try:
        model = load_model(model_path)
        X_train, X_test, y_train, y_test, scaler = prepare_data(df, feature_cols)
        last_sequence = X_test[-1].reshape(1, X_test.shape[1], X_test.shape[2])
        prediction_prob = model.predict(last_sequence, verbose=0)[0][0]
        prediction_class = 1 if prediction_prob > 0.5 else 0
        
        print(f"\n🤖 AI MODEL PREDICTION")
        print(f"{'─'*70}")
        print(f"Next Day Trend: {'📈 UP' if prediction_class == 1 else '📉 DOWN'}")
        print(f"Confidence: {prediction_prob*100:.2f}%")
        
        # Adjust score based on model
        if prediction_class == 1:
            total_score += 2
        else:
            total_score -= 2
    except:
        print(f"\n⚠️  Model not found. Using technical analysis only.")
    
    # Generate recommendation
    print(f"\n💡 SWING TRADING RECOMMENDATION")
    print(f"{'='*70}")
    
    if total_score >= 6:
        recommendation = "🟢 STRONG BUY"
        action = "Enter swing position with 70-80% of planned capital"
        stop_loss = current['Close'] * 0.95
        target_1 = current['Close'] * 1.05
        target_2 = current['Close'] * 1.10
        holding_period = "3-7 days"
    elif total_score >= 3:
        recommendation = "🟢 BUY"
        action = "Enter swing position with 50-60% of planned capital"
        stop_loss = current['Close'] * 0.96
        target_1 = current['Close'] * 1.04
        target_2 = current['Close'] * 1.08
        holding_period = "5-10 days"
    elif total_score >= 0:
        recommendation = "🟡 HOLD/WATCH"
        action = "Wait for better entry point or hold existing positions"
        stop_loss = current['Close'] * 0.97
        target_1 = current['Close'] * 1.03
        target_2 = current['Close'] * 1.06
        holding_period = "Monitor daily"
    elif total_score >= -3:
        recommendation = "🔴 SELL"
        action = "Exit 50-60% of swing positions"
        stop_loss = None
        target_1 = None
        target_2 = None
        holding_period = "Exit within 1-2 days"
    else:
        recommendation = "🔴 STRONG SELL"
        action = "Exit all swing positions immediately"
        stop_loss = None
        target_1 = None
        target_2 = None
        holding_period = "Exit today"
    
    print(f"\nRecommendation: {recommendation}")
    print(f"Signal Strength: {total_score}/12")
    print(f"\nAction: {action}")
    
    if stop_loss:
        print(f"\n📍 PRICE TARGETS")
        print(f"{'─'*70}")
        print(f"Entry Price: ₹{current['Close']:.2f}")
        print(f"Stop Loss: ₹{stop_loss:.2f} ({((stop_loss/current['Close']-1)*100):.1f}%)")
        print(f"Target 1: ₹{target_1:.2f} ({((target_1/current['Close']-1)*100):.1f}%)")
        print(f"Target 2: ₹{target_2:.2f} ({((target_2/current['Close']-1)*100):.1f}%)")
        print(f"Holding Period: {holding_period}")
        
        # Risk-Reward Ratio
        risk = current['Close'] - stop_loss
        reward = target_1 - current['Close']
        rr_ratio = reward / risk if risk > 0 else 0
        print(f"Risk-Reward Ratio: 1:{rr_ratio:.2f}")
    
    print(f"\n⚠️  RISK DISCLAIMER")
    print(f"{'─'*70}")
    print(f"• This is NOT financial advice")
    print(f"• Past performance doesn't guarantee future results")
    print(f"• Always use stop-loss orders")
    print(f"• Never invest more than you can afford to lose")
    print(f"• Do your own research before trading")
    
    print(f"\n{'='*70}\n")
    
    return {
        'ticker': ticker,
        'recommendation': recommendation,
        'score': total_score,
        'action': action,
        'entry': current['Close'],
        'stop_loss': stop_loss,
        'target_1': target_1,
        'target_2': target_2,
        'holding_period': holding_period
    }

def main():
    parser = argparse.ArgumentParser(description='Swing Trading Recommendation')
    parser.add_argument('--ticker', type=str, default='RELIANCE.NS',
                        help='Stock ticker symbol')
    parser.add_argument('--model', type=str, default='stock_lstm_model.h5',
                        help='Path to trained model')
    
    args = parser.parse_args()
    generate_swing_recommendation(args.ticker, args.model)

if __name__ == '__main__':
    main()
