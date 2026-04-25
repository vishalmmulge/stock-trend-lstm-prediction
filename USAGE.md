# Usage Guide - Stock Trend Prediction

## Quick Start (Recommended)

The fastest way to get started:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests to verify setup
python test_project.py

# Train model and see results
python quick_start.py
```

## Detailed Usage

### 1. Training the Model

#### Basic Training
```bash
python -m src.train
```

This will:
- Download RELIANCE.NS data (5 years)
- Calculate technical indicators
- Train LSTM model (10 epochs)
- Save model as `stock_lstm_model.h5`
- Generate `training_history.png`

#### Custom Training
Edit `src/train.py` to customize:

```python
# Change stock ticker
train_model(ticker='AAPL')  # Apple
train_model(ticker='TSLA')  # Tesla
train_model(ticker='TCS.NS')  # TCS

# Change training parameters
train_model(ticker='RELIANCE.NS', epochs=20, batch_size=64)
```

### 2. Making Predictions

#### Predict Next Day Trend
```bash
# Default (RELIANCE.NS)
python predict.py

# Custom ticker
python predict.py --ticker AAPL
python predict.py --ticker TCS.NS

# Custom model path
python predict.py --ticker AAPL --model my_model.h5
```

Output example:
```
============================================================
PREDICTION FOR RELIANCE.NS
============================================================
Current Date: 2024-01-15
Current Close Price: ₹2,450.50

Prediction for Next Day:
  Trend: 📈 UP
  Confidence: 67.23%
  Class: 1

Current Technical Indicators:
  RSI: 58.45
  SMA20: ₹2,430.20
  SMA50: ₹2,410.80
  MACD: 12.34
============================================================
```

### 3. Backtesting

```bash
python -m src.backtest
```

This simulates trading with ₹100,000 and compares:
- Your LSTM strategy
- Buy & Hold strategy

Output example:
```
==================================================
BACKTEST RESULTS
==================================================
Initial Capital: ₹100,000.00
Final Portfolio Value: ₹125,450.00
Strategy Return: 25.45%

Buy & Hold Value: ₹118,200.00
Buy & Hold Return: 18.20%

Outperformance: 7.25%
==================================================
```

### 4. Streamlit Web App

```bash
streamlit run app.py
```

Then open browser at `http://localhost:8501`

**Features:**
- Enter any stock ticker
- View price charts
- See technical indicators
- Get next-day prediction
- View backtest results

### 5. Jupyter Notebook

For exploratory analysis:

```bash
jupyter notebook notebooks/exploration.ipynb
```

This notebook includes:
- Data loading and visualization
- Feature engineering walkthrough
- Model training step-by-step
- Evaluation metrics
- Interactive plots

## Advanced Usage

### Custom Time Windows

Edit `src/model.py`:

```python
# Change from 60 days to 90 days
X_train, X_test, y_train, y_test, scaler = prepare_data(
    df, feature_cols, time_steps=90
)
```

### Custom Features

Edit `src/features.py` to add new indicators:

```python
def add_technical_indicators(df):
    # ... existing code ...
    
    # Add Bollinger Bands
    df['BB_upper'] = df['SMA20'] + 2 * df['Close'].rolling(20).std()
    df['BB_lower'] = df['SMA20'] - 2 * df['Close'].rolling(20).std()
    
    # Add ATR
    high_low = df['High'] - df['Low']
    df['ATR'] = high_low.rolling(14).mean()
    
    return df
```

### Custom Model Architecture

Edit `src/model.py`:

```python
def build_lstm_model(input_shape):
    model = Sequential([
        LSTM(128, return_sequences=True, input_shape=input_shape),
        Dropout(0.3),
        LSTM(64, return_sequences=True),
        Dropout(0.3),
        LSTM(32),
        Dropout(0.2),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    return model
```

### Batch Predictions

Create a script to predict multiple stocks:

```python
from predict import predict_next_day

tickers = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS']

for ticker in tickers:
    try:
        result = predict_next_day(ticker)
        print(f"{ticker}: {result['prediction']}")
    except Exception as e:
        print(f"{ticker}: Error - {e}")
```

## Configuration

Edit `config.py` to change default settings:

```python
# Data
DEFAULT_TICKER = 'AAPL'  # Change default stock
DATA_PERIOD = '10y'      # More historical data

# Model
EPOCHS = 20              # More training epochs
BATCH_SIZE = 64          # Larger batch size
TIME_STEPS = 90          # Longer lookback period

# Backtesting
INITIAL_CAPITAL = 500000  # ₹5 lakhs
```

## Troubleshooting

### Issue: "No module named 'src'"
**Solution:** Run from project root directory

```bash
cd stock-trend-lstm
python -m src.train
```

### Issue: "Model file not found"
**Solution:** Train the model first

```bash
python -m src.train
```

### Issue: "No data available"
**Solution:** Check internet connection and ticker symbol

```bash
# Verify ticker on Yahoo Finance
# Indian stocks: Add .NS (e.g., RELIANCE.NS)
# US stocks: Use symbol directly (e.g., AAPL)
```

### Issue: Low accuracy
**Solutions:**
1. Train for more epochs
2. Use more historical data
3. Add more features
4. Try different model architectures
5. Adjust time_steps parameter

## Performance Tips

1. **Use GPU for faster training:**
   ```bash
   pip install tensorflow-gpu
   ```

2. **Cache data to avoid re-downloading:**
   ```python
   df.to_csv('data/cached_data.csv')
   df = pd.read_csv('data/cached_data.csv')
   ```

3. **Use smaller batch size if running out of memory:**
   ```python
   train_model(batch_size=16)
   ```

## Examples

### Example 1: Train on US Stock
```bash
# Edit src/train.py, change ticker to 'AAPL'
python -m src.train
python predict.py --ticker AAPL
```

### Example 2: Compare Multiple Stocks
```python
# compare_stocks.py
from predict import predict_next_day

stocks = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS']
results = []

for stock in stocks:
    result = predict_next_day(stock)
    results.append(result)

# Print comparison
for r in results:
    print(f"{r['ticker']}: {r['prediction']} ({r['confidence']*100:.1f}%)")
```

### Example 3: Export Predictions to CSV
```python
import pandas as pd
from predict import predict_next_day

tickers = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS']
predictions = []

for ticker in tickers:
    result = predict_next_day(ticker)
    predictions.append(result)

df = pd.DataFrame(predictions)
df.to_csv('predictions.csv', index=False)
print("Predictions saved to predictions.csv")
```

## Next Steps

1. Experiment with different stocks
2. Try different time periods
3. Add more technical indicators
4. Tune hyperparameters
5. Implement risk management
6. Add stop-loss logic
7. Create ensemble models
8. Deploy to cloud (AWS, GCP, Azure)

## Support

For issues or questions:
1. Check README.md
2. Review this USAGE.md
3. Run test_project.py to diagnose issues
4. Check configuration in config.py
