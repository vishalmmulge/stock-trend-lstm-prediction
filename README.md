# 📈 Stock Trend Prediction using LSTM + Technical Indicators

A complete machine learning capstone project that predicts next-day stock trends using LSTM neural networks combined with technical indicators.

## 🎯 Problem Statement

Predict whether the next day's closing price will be higher or lower than today's closing price:
- **Output 1**: Next day Close > Today's Close (UP trend)
- **Output 0**: Next day Close ≤ Today's Close (DOWN trend)

## 🚀 Features

### Technical Indicators
- Daily Return
- Simple Moving Averages (SMA20, SMA50)
- Relative Strength Index (RSI-14)
- MACD and MACD Signal
- Volume Change %

### Model Architecture
- LSTM(64, return_sequences=True) + Dropout(0.2)
- LSTM(32) + Dropout(0.2)
- Dense(16, relu)
- Dense(1, sigmoid)

### Backtesting Strategy
- Initial Capital: ₹100,000
- Buy when model predicts UP (1)
- Stay in cash when model predicts DOWN (0)
- Compare against Buy & Hold strategy

## 📁 Project Structure

```
stock-trend-lstm/
│
├── data/                      # Data storage
├── notebooks/                 # Jupyter notebooks for exploration
├── src/
│   ├── data_loader.py        # Load stock data from Yahoo Finance
│   ├── features.py           # Technical indicator calculations
│   ├── model.py              # LSTM model architecture
│   ├── train.py              # Training pipeline
│   └── backtest.py           # Backtesting strategy
│
├── app.py                    # Streamlit web application
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🛠️ Setup Instructions

### 1. Clone or Download the Project

```bash
cd stock-trend-lstm
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🎓 How to Use

### Training the Model

Run the training script to train the LSTM model:

```bash
python -m src.train
```

**What it does:**
- Downloads 5 years of RELIANCE.NS stock data from Yahoo Finance
- Calculates technical indicators
- Creates 60-day time windows
- Trains LSTM model for 10 epochs
- Saves model as `stock_lstm_model.h5`
- Generates training history plots
- Prints classification report and confusion matrix

**Expected Output:**
- Training/validation accuracy curves
- Loss curves
- Classification metrics
- Saved model file

### Running Backtest

Test the trading strategy:

```bash
python -m src.backtest
```

**What it does:**
- Loads trained model
- Simulates trading with ₹100,000 initial capital
- Compares strategy returns vs buy-and-hold
- Prints detailed backtest results

### Running Streamlit App

Launch the interactive web application:

```bash
streamlit run app.py
```

**Features:**
- Input any stock ticker (RELIANCE.NS, AAPL, TSLA, TCS.NS, etc.)
- View stock price history
- Visualize technical indicators (SMA, RSI, MACD)
- Get next-day trend prediction
- See backtest performance metrics
- Compare strategy vs buy-and-hold

**Access the app at:** `http://localhost:8501`

## 📊 Model Explanation

### Data Preprocessing
1. **Feature Engineering**: Calculate 9 technical indicators
2. **Normalization**: MinMaxScaler to scale features to [0,1]
3. **Sequence Creation**: Use 60 days of historical data to predict day 61
4. **Train-Test Split**: 80% training, 20% testing (time-based split)

### LSTM Architecture
- **Layer 1**: LSTM with 64 units, returns sequences
- **Layer 2**: Dropout (20%) to prevent overfitting
- **Layer 3**: LSTM with 32 units
- **Layer 4**: Dropout (20%)
- **Layer 5**: Dense layer with 16 neurons (ReLU activation)
- **Output**: Dense layer with 1 neuron (Sigmoid activation)

### Training Configuration
- **Optimizer**: Adam
- **Loss Function**: Binary Crossentropy
- **Metrics**: Accuracy
- **Epochs**: 10
- **Batch Size**: 32
- **Validation Split**: 20%

## 📈 Results & Limitations

### Expected Performance
- Training Accuracy: ~55-65%
- Test Accuracy: ~50-60%
- Backtest returns vary based on market conditions

### Limitations
1. **Market Efficiency**: Stock markets are highly efficient; predicting trends is inherently difficult
2. **Overfitting Risk**: Model may overfit to historical patterns that don't repeat
3. **Transaction Costs**: Real-world trading involves fees and slippage not modeled here
4. **Binary Classification**: Simplifies complex market dynamics into UP/DOWN
5. **No Fundamental Analysis**: Only uses technical indicators, ignores news/events
6. **Look-Ahead Bias**: Careful to avoid using future information in features

### Improvements to Consider
- Add more features (sentiment analysis, fundamental ratios)
- Experiment with different architectures (GRU, Transformer)
- Implement proper risk management (stop-loss, position sizing)
- Use ensemble methods
- Add market regime detection
- Incorporate transaction costs in backtesting

## 🔧 Customization

### Change Stock Ticker
Edit the ticker in `src/train.py` or use the Streamlit app:
```python
train_model(ticker='AAPL')  # For Apple
train_model(ticker='TCS.NS')  # For TCS
```

### Adjust Time Window
Modify the `time_steps` parameter in `src/model.py`:
```python
X_train, X_test, y_train, y_test, scaler = prepare_data(df, feature_cols, time_steps=90)
```

### Change Training Parameters
Edit `src/train.py`:
```python
train_model(ticker='RELIANCE.NS', epochs=20, batch_size=64)
```

## 📚 Dependencies

- **yfinance**: Download stock data from Yahoo Finance
- **pandas**: Data manipulation
- **numpy**: Numerical operations
- **scikit-learn**: Preprocessing and metrics
- **tensorflow**: Deep learning framework
- **matplotlib**: Plotting training curves
- **streamlit**: Web application framework
- **plotly**: Interactive charts

## ⚠️ Disclaimer

This project is for educational purposes only. It is NOT financial advice. Do not use this model for actual trading without proper risk management and understanding of financial markets. Past performance does not guarantee future results.

## 📝 License

This project is open-source and available for educational use.

## 👨‍💻 Author

Built as a capstone project demonstrating:
- Time series forecasting with LSTM
- Feature engineering for financial data
- Model evaluation and backtesting
- Web deployment with Streamlit

---

**Happy Learning! 🚀**
