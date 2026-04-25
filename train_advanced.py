import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from src.data_loader import load_stock_data
from src.features_advanced import prepare_advanced_features
from src.model_advanced import build_advanced_lstm_model, prepare_data_advanced, get_callbacks

def train_advanced_model(ticker='RELIANCE.NS', epochs=30, batch_size=32):
    """Train advanced LSTM model with more features"""
    print(f"Loading data for {ticker}...")
    df = load_stock_data(ticker)
    
    print("Preparing advanced features...")
    df, feature_cols = prepare_advanced_features(df)
    print(f"Using {len(feature_cols)} features")
    
    print("Preparing sequences...")
    X_train, X_test, y_train, y_test, scaler = prepare_data_advanced(df, feature_cols)
    
    print(f"Training samples: {len(X_train)}, Test samples: {len(X_test)}")
    print(f"Input shape: {X_train.shape}")
    
    print("Building advanced model...")
    model = build_advanced_lstm_model((X_train.shape[1], X_train.shape[2]))
    model.summary()
    
    print("Training model with callbacks...")
    callbacks = get_callbacks()
    
    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_split=0.2,
        callbacks=callbacks,
        verbose=1
    )
    
    print("\nEvaluating model...")
    y_pred_prob = model.predict(X_test)
    y_pred = (y_pred_prob > 0.5).astype(int)
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # ROC AUC Score
    auc = roc_auc_score(y_test, y_pred_prob)
    print(f"\nROC AUC Score: {auc:.4f}")
    
    # Plot training history
    plot_training_history(history)
    
    # Save model
    model.save('stock_lstm_advanced.h5')
    print("\nAdvanced model saved as 'stock_lstm_advanced.h5'")
    
    return model, history, df, scaler, feature_cols

def plot_training_history(history):
    """Plot accuracy and loss curves"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1.plot(history.history['accuracy'], label='Train Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Val Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    ax1.grid(True)
    
    ax2.plot(history.history['loss'], label='Train Loss')
    ax2.plot(history.history['val_loss'], label='Val Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('training_history_advanced.png')
    print("Training history saved as 'training_history_advanced.png'")
    plt.close()

if __name__ == '__main__':
    train_advanced_model(ticker='RELIANCE.NS', epochs=50, batch_size=32)
