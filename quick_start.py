"""
Quick Start Script for Stock Trend Prediction
Run this to train the model and see results quickly
"""

import sys
from src.train import train_model
from src.backtest import backtest_strategy, print_backtest_results
from src.model import prepare_data
from src.features import prepare_features
from src.data_loader import load_stock_data

def main():
    print("="*60)
    print("STOCK TREND PREDICTION - QUICK START")
    print("="*60)
    
    # Train model
    print("\n[1/3] Training LSTM Model...")
    model, history, df, scaler, feature_cols = train_model(
        ticker='RELIANCE.NS',
        epochs=10,
        batch_size=32
    )
    
    # Prepare test data
    print("\n[2/3] Preparing test data...")
    X_train, X_test, y_train, y_test, _ = prepare_data(df, feature_cols)
    
    # Run backtest
    print("\n[3/3] Running backtest...")
    results = backtest_strategy(model, df, X_test, y_test)
    print_backtest_results(results)
    
    print("\n" + "="*60)
    print("QUICK START COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Check 'training_history.png' for training curves")
    print("2. Run 'streamlit run app.py' to launch web app")
    print("3. Explore 'notebooks/exploration.ipynb' for detailed analysis")
    print("\n")

if __name__ == '__main__':
    main()
