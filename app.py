import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow warnings

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tensorflow.keras.models import load_model
import os

from src.data_loader import load_stock_data
from src.features import prepare_features
from src.model import prepare_data, create_lstm_sequences
from src.backtest import backtest_strategy, print_backtest_results
from swing_trading import calculate_swing_signals, generate_swing_recommendation

st.set_page_config(page_title="Stock Trend Prediction", layout="wide")

st.title("📈 Stock Trend Prediction using LSTM")
st.markdown("Predict next-day stock trends using LSTM with technical indicators")

# Sidebar
st.sidebar.header("Configuration")
ticker = st.sidebar.text_input("Stock Ticker", value="RELIANCE.NS")
period = st.sidebar.selectbox("Data Period", ["1y", "2y", "3y", "5y"], index=3)

if st.sidebar.button("Load & Predict"):
    with st.spinner("Loading data..."):
        try:
            # Load data
            df = load_stock_data(ticker, period)
            st.success(f"Loaded {len(df)} days of data for {ticker}")
            
            # Prepare features
            df, feature_cols = prepare_features(df)
            
            # Display stock price chart
            st.subheader("📊 Stock Price History")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name='Close Price'))
            fig.update_layout(xaxis_title="Date", yaxis_title="Price", height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            # Display technical indicators
            st.subheader("📉 Technical Indicators")
            fig = make_subplots(rows=3, cols=1, subplot_titles=("SMA", "RSI", "MACD"))
            
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Close'), row=1, col=1)
            fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA20'], name='SMA20'), row=1, col=1)
            fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA50'], name='SMA50'), row=1, col=1)
            
            fig.add_trace(go.Scatter(x=df['Date'], y=df['RSI'], name='RSI'), row=2, col=1)
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)
            
            fig.add_trace(go.Scatter(x=df['Date'], y=df['MACD'], name='MACD'), row=3, col=1)
            fig.add_trace(go.Scatter(x=df['Date'], y=df['MACD_Signal'], name='Signal'), row=3, col=1)
            
            fig.update_layout(height=800, showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
            
            # Load or train model
            if os.path.exists('stock_lstm_model.h5'):
                model = load_model('stock_lstm_model.h5')
                st.info("Loaded pre-trained model")
            else:
                st.warning("No pre-trained model found. Please train the model first using train.py")
                st.stop()
            
            # Prepare data for prediction
            X_train, X_test, y_train, y_test, scaler = prepare_data(df, feature_cols)
            
            # Make prediction for next day
            last_sequence = X_test[-1].reshape(1, X_test.shape[1], X_test.shape[2])
            prediction = model.predict(last_sequence)[0][0]
            prediction_class = 1 if prediction > 0.5 else 0
            
            # Display prediction
            st.subheader("🔮 Next Day Prediction")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Current Close", f"₹{df.iloc[-1]['Close']:.2f}")
            
            with col2:
                trend = "📈 UP" if prediction_class == 1 else "📉 DOWN"
                st.metric("Predicted Trend", trend)
            
            with col3:
                st.metric("Confidence", f"{prediction*100:.2f}%")
            
            # Swing Trading Recommendation
            st.subheader("🎯 Swing Trading Recommendation")
            
            signals = calculate_swing_signals(df)
            total_score = (signals['trend_score'] + signals['rsi_score'] + 
                          signals['macd_score'] + signals['volume_score'])
            
            if prediction_class == 1:
                total_score += 2
            else:
                total_score -= 2
            
            # Generate recommendation
            if total_score >= 6:
                recommendation = "🟢 STRONG BUY"
                rec_color = "green"
            elif total_score >= 3:
                recommendation = "🟢 BUY"
                rec_color = "green"
            elif total_score >= 0:
                recommendation = "🟡 HOLD/WATCH"
                rec_color = "orange"
            elif total_score >= -3:
                recommendation = "🔴 SELL"
                rec_color = "red"
            else:
                recommendation = "🔴 STRONG SELL"
                rec_color = "red"
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Recommendation", recommendation)
            
            with col2:
                st.metric("Signal Strength", f"{total_score}/12")
            
            with col3:
                st.metric("Trend", signals['trend'])
            
            with col4:
                st.metric("RSI Signal", signals['rsi_signal'])
            
            # Price Targets
            if total_score >= 0:
                current_price = df.iloc[-1]['Close']
                stop_loss = current_price * 0.95
                target_1 = current_price * 1.05
                target_2 = current_price * 1.10
                
                st.write("**📍 Price Targets:**")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Stop Loss", f"₹{stop_loss:.2f}", f"-5.0%")
                
                with col2:
                    st.metric("Target 1", f"₹{target_1:.2f}", f"+5.0%")
                
                with col3:
                    st.metric("Target 2", f"₹{target_2:.2f}", f"+10.0%")
            
            # Backtest results
            st.subheader("💰 Backtest Results")
            results = backtest_strategy(model, df, X_test, y_test)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Strategy Return", f"{results['strategy_return']:.2f}%")
                st.metric("Final Portfolio Value", f"₹{results['final_value']:,.2f}")
            
            with col2:
                st.metric("Buy & Hold Return", f"{results['buy_hold_return']:.2f}%")
                st.metric("Outperformance", f"{results['strategy_return'] - results['buy_hold_return']:.2f}%")
            
            # Portfolio value chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=results['portfolio_values'], mode='lines', name='Strategy Portfolio'))
            fig.update_layout(title="Portfolio Value Over Time", xaxis_title="Days", yaxis_title="Value (₹)", height=400)
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Information section
st.sidebar.markdown("---")
st.sidebar.subheader("About")
st.sidebar.info("""
This app predicts stock trends using:
- LSTM Neural Network
- Technical Indicators (SMA, RSI, MACD)
- 60-day time windows

**How to use:**
1. Enter stock ticker (e.g., RELIANCE.NS, AAPL, TSLA)
2. Select data period
3. Click 'Load & Predict'
""")

st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit & TensorFlow")
