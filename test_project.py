"""
Test script to verify all components of the project
"""

import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    try:
        import yfinance
        import pandas
        import numpy
        import sklearn
        import tensorflow
        import matplotlib
        import streamlit
        import plotly
        print("✓ All packages imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_data_loader():
    """Test data loading functionality"""
    print("\nTesting data loader...")
    try:
        from src.data_loader import load_stock_data
        df = load_stock_data('RELIANCE.NS', period='1mo')
        assert len(df) > 0, "No data loaded"
        assert 'Close' in df.columns, "Missing Close column"
        print(f"✓ Data loader works - loaded {len(df)} rows")
        return True
    except Exception as e:
        print(f"✗ Data loader error: {e}")
        return False

def test_features():
    """Test feature engineering"""
    print("\nTesting feature engineering...")
    try:
        from src.data_loader import load_stock_data
        from src.features import prepare_features
        
        df = load_stock_data('RELIANCE.NS', period='1y')
        df, feature_cols = prepare_features(df)
        
        assert 'SMA20' in df.columns, "Missing SMA20"
        assert 'RSI' in df.columns, "Missing RSI"
        assert 'MACD' in df.columns, "Missing MACD"
        assert 'Target' in df.columns, "Missing Target"
        
        print(f"✓ Feature engineering works - {len(feature_cols)} features created")
        return True
    except Exception as e:
        print(f"✗ Feature engineering error: {e}")
        return False

def test_model():
    """Test model building"""
    print("\nTesting model building...")
    try:
        from src.model import build_lstm_model
        
        model = build_lstm_model((60, 9))
        assert model is not None, "Model not created"
        assert len(model.layers) == 6, "Incorrect number of layers"
        
        print("✓ Model building works")
        return True
    except Exception as e:
        print(f"✗ Model building error: {e}")
        return False

def test_data_preparation():
    """Test data preparation for LSTM"""
    print("\nTesting data preparation...")
    try:
        from src.data_loader import load_stock_data
        from src.features import prepare_features
        from src.model import prepare_data
        
        df = load_stock_data('RELIANCE.NS', period='2y')
        df, feature_cols = prepare_features(df)
        X_train, X_test, y_train, y_test, scaler = prepare_data(df, feature_cols)
        
        assert len(X_train) > 0, "No training data"
        assert len(X_test) > 0, "No test data"
        assert X_train.shape[1] == 60, "Incorrect time steps"
        
        print(f"✓ Data preparation works - Train: {len(X_train)}, Test: {len(X_test)}")
        return True
    except Exception as e:
        print(f"✗ Data preparation error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("RUNNING PROJECT TESTS")
    print("="*60)
    
    tests = [
        test_imports,
        test_data_loader,
        test_features,
        test_model,
        test_data_preparation
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "="*60)
    print(f"RESULTS: {sum(results)}/{len(results)} tests passed")
    print("="*60)
    
    if all(results):
        print("\n✓ All tests passed! Project is ready to use.")
        print("\nNext steps:")
        print("1. Run: python quick_start.py")
        print("2. Or run: python -m src.train")
        print("3. Then: streamlit run app.py")
    else:
        print("\n✗ Some tests failed. Please check the errors above.")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")

if __name__ == '__main__':
    main()
