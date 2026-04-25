import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from src.data_loader import load_stock_data
from src.features import prepare_features
from src.model import prepare_data

def backtest_strategy(model, df, X_test, y_test, initial_capital=100000):
    """Backtest trading strategy"""
    predictions = (model.predict(X_test) > 0.5).astype(int).flatten()
    
    # Get corresponding dates and prices
    time_steps = 60
    train_split = 0.8
    split_idx = int((len(df) - time_steps) * train_split)
    test_start_idx = split_idx + time_steps
    
    test_df = df.iloc[test_start_idx:test_start_idx + len(predictions)].copy()
    test_df['Prediction'] = predictions
    
    # Strategy simulation
    capital = initial_capital
    position = 0
    portfolio_values = []
    
    for i in range(len(test_df) - 1):
        current_price = test_df.iloc[i]['Close']
        next_price = test_df.iloc[i + 1]['Close']
        pred = test_df.iloc[i]['Prediction']
        
        if pred == 1:  # Buy signal
            if position == 0:
                position = capital / current_price
                capital = 0
        else:  # Sell signal
            if position > 0:
                capital = position * current_price
                position = 0
        
        # Calculate portfolio value
        if position > 0:
            portfolio_value = position * current_price
        else:
            portfolio_value = capital
        
        portfolio_values.append(portfolio_value)
    
    # Final portfolio value
    final_price = test_df.iloc[-1]['Close']
    if position > 0:
        final_value = position * final_price
    else:
        final_value = capital
    
    # Buy and hold strategy
    buy_hold_shares = initial_capital / test_df.iloc[0]['Close']
    buy_hold_value = buy_hold_shares * test_df.iloc[-1]['Close']
    
    # Results
    strategy_return = ((final_value - initial_capital) / initial_capital) * 100
    buy_hold_return = ((buy_hold_value - initial_capital) / initial_capital) * 100
    
    results = {
        'initial_capital': initial_capital,
        'final_value': final_value,
        'strategy_return': strategy_return,
        'buy_hold_value': buy_hold_value,
        'buy_hold_return': buy_hold_return,
        'portfolio_values': portfolio_values,
        'test_df': test_df
    }
    
    return results

def print_backtest_results(results):
    """Print backtest results"""
    print("\n" + "="*50)
    print("BACKTEST RESULTS")
    print("="*50)
    print(f"Initial Capital: ₹{results['initial_capital']:,.2f}")
    print(f"Final Portfolio Value: ₹{results['final_value']:,.2f}")
    print(f"Strategy Return: {results['strategy_return']:.2f}%")
    print(f"\nBuy & Hold Value: ₹{results['buy_hold_value']:,.2f}")
    print(f"Buy & Hold Return: {results['buy_hold_return']:.2f}%")
    print(f"\nOutperformance: {results['strategy_return'] - results['buy_hold_return']:.2f}%")
    print("="*50)

if __name__ == '__main__':
    # Load model
    model = load_model('stock_lstm_model.h5')
    
    # Load and prepare data
    df = load_stock_data('RELIANCE.NS')
    df, feature_cols = prepare_features(df)
    X_train, X_test, y_train, y_test, scaler = prepare_data(df, feature_cols)
    
    # Run backtest
    results = backtest_strategy(model, df, X_test, y_test)
    print_backtest_results(results)
