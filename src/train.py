import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix
from src.data_loader import load_stock_data
from src.features import prepare_features
from src.model import build_lstm_model, prepare_data

def train_model(ticker='RELIANCE.NS', epochs=10, batch_size=32):
    """Train LSTM model on stock data"""
    print(f"Loading data for {ticker}...")
    df = load_stock_data(ticker)
    
    print("Preparing features...")
    df, feature_cols = prepare_features(df)
    
    print("Preparing sequences...")
    X_train, X_test, y_train, y_test, scaler = prepare_data(df, feature_cols)
    
    print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")
    print(f"Input shape: {X_train.shape}")
    
    print("Building model...")
    model = build_lstm_model((X_train.shape[1], X_train.shape[2]))
    model.summary()
    
    print("Training model...")
    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=0.2,
        verbose=1
    )
    
    print("\nEvaluating model...")
    y_pred = (model.predict(X_test) > 0.5).astype(int)
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # Plot training history
    plot_training_history(history)
    
    # Save model
    model.save('stock_lstm_model.h5')
    print("\nModel saved as 'stock_lstm_model.h5'")
    
    return model, history, df, scaler, feature_cols

def plot_training_history(history):
    """Plot accuracy and loss curves"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Accuracy
    ax1.plot(history.history['accuracy'], label='Train Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Val Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True)
    
    # Loss
    ax2.plot(history.history['loss'], label='Train Loss')
    ax2.plot(history.history['val_loss'], label='Val Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('training_history.png')
    print("Training history saved as 'training_history.png'")
    plt.close()

if __name__ == '__main__':
    # Change ticker here to train on any stock
    train_model(ticker='RELIANCE.NS', epochs=50)  # Increased to 50 epochs
