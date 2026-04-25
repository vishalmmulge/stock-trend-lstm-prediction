"""
Configuration file for Stock Trend Prediction project
"""

# Data Configuration
DEFAULT_TICKER = 'RELIANCE.NS'
DATA_PERIOD = '5y'
TRAIN_TEST_SPLIT = 0.8

# Feature Engineering
TIME_STEPS = 60  # Number of days to look back
SMA_SHORT = 20
SMA_LONG = 50
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# Model Configuration
LSTM_UNITS_1 = 64
LSTM_UNITS_2 = 32
DENSE_UNITS = 16
DROPOUT_RATE = 0.2

# Training Configuration
EPOCHS = 50
BATCH_SIZE = 32
VALIDATION_SPLIT = 0.2
OPTIMIZER = 'adam'
LOSS = 'binary_crossentropy'

# Backtesting Configuration
INITIAL_CAPITAL = 100000  # ₹100,000

# File Paths
MODEL_PATH = 'stock_lstm_model.h5'
TRAINING_PLOT_PATH = 'training_history.png'
