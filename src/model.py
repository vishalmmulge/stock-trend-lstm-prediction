import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

def create_lstm_sequences(data, target, time_steps=60):
    """Create sequences for LSTM input"""
    X, y = [], []
    for i in range(time_steps, len(data)):
        X.append(data[i-time_steps:i])
        y.append(target[i])
    return np.array(X), np.array(y)

def build_lstm_model(input_shape):
    """Build LSTM model architecture"""
    model = Sequential([
        LSTM(64, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(32),
        Dropout(0.2),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

def prepare_data(df, feature_cols, time_steps=60, train_split=0.8):
    """Prepare and scale data for LSTM"""
    # Scale features
    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(df[feature_cols])
    
    # Get target
    target = df['Target'].values
    
    # Create sequences
    X, y = create_lstm_sequences(scaled_features, target, time_steps)
    
    # Time-based split
    split_idx = int(len(X) * train_split)
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y[:split_idx], y[split_idx:]
    
    return X_train, X_test, y_train, y_test, scaler
