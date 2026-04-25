# Getting Started - Stock Trend Prediction

Welcome! This guide will help you get the project running in 5 minutes.

## 🎯 What This Project Does

Predicts whether a stock will go **UP** ⬆️ or **DOWN** ⬇️ tomorrow using:
- 5 years of historical data
- 9 technical indicators (SMA, RSI, MACD, etc.)
- LSTM neural network
- 60-day time windows

## ⚡ Quick Start (5 Minutes)

### Step 1: Open Terminal
Navigate to the project folder:
```bash
cd c:\Users\visha\Desktop\LIFE\stock-trend-lstm
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Wait 2-3 minutes for installation...**

### Step 3: Run Quick Start
```bash
python quick_start.py
```

**This will:**
- Download RELIANCE.NS stock data
- Train the LSTM model (10 epochs)
- Show accuracy and loss curves
- Run backtest simulation
- Display results

**Wait 5-10 minutes for training...**

### Step 4: Make a Prediction
```bash
python predict.py
```

**Output:**
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
============================================================
```

### Step 5: Launch Web App
```bash
streamlit run app.py
```

**Opens browser at:** http://localhost:8501

**Try it:**
- Enter different stock tickers (AAPL, TSLA, TCS.NS)
- View interactive charts
- Get predictions
- See backtest results

## 🎓 What You Just Did

1. ✅ Trained an LSTM neural network
2. ✅ Predicted stock trends
3. ✅ Backtested a trading strategy
4. ✅ Deployed a web application

## 📚 Next Steps

### Learn More
- Read [README.md](README.md) for detailed documentation
- Read [USAGE.md](USAGE.md) for advanced usage
- Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for technical details

### Try Different Stocks
```bash
# US Stocks
python predict.py --ticker AAPL
python predict.py --ticker TSLA
python predict.py --ticker GOOGL

# Indian Stocks
python predict.py --ticker TCS.NS
python predict.py --ticker INFY.NS
python predict.py --ticker HDFCBANK.NS
```

### Explore the Code
```bash
# Open Jupyter notebook
jupyter notebook notebooks/exploration.ipynb
```

### Customize the Model
Edit `config.py` to change:
- Number of epochs
- Batch size
- Time window (60 days)
- Initial capital for backtesting

## 🔧 Troubleshooting

### Issue: "pip not found"
**Solution:** Install Python from python.org

### Issue: "Module not found"
**Solution:** 
```bash
pip install -r requirements.txt
```

### Issue: "Model file not found"
**Solution:** Train the model first
```bash
python -m src.train
```

### Issue: "No data available"
**Solution:** Check internet connection and ticker symbol
- Indian stocks need .NS suffix (RELIANCE.NS)
- US stocks use symbol directly (AAPL)

### Issue: Training is slow
**Solution:** 
- Reduce epochs in config.py
- Use smaller batch size
- Or just wait (5-10 minutes is normal)

## 📊 Understanding the Output

### Training Output
```
Epoch 1/10
45/45 [==============================] - 15s 334ms/step
loss: 0.6891 - accuracy: 0.5234 - val_loss: 0.6823 - val_accuracy: 0.5456
```

- **loss:** Lower is better (target: < 0.5)
- **accuracy:** Higher is better (target: > 55%)
- **val_accuracy:** Validation accuracy (should be close to training accuracy)

### Prediction Output
```
Trend: 📈 UP
Confidence: 67.23%
```

- **UP:** Model predicts price will increase tomorrow
- **DOWN:** Model predicts price will decrease tomorrow
- **Confidence:** How sure the model is (50% = uncertain, 90% = very sure)

### Backtest Output
```
Strategy Return: 25.45%
Buy & Hold Return: 18.20%
Outperformance: 7.25%
```

- **Strategy Return:** Your LSTM strategy profit
- **Buy & Hold Return:** If you just bought and held
- **Outperformance:** How much better your strategy is

## 🎯 Project Files Explained

| File | Purpose |
|------|---------|
| `src/data_loader.py` | Downloads stock data from Yahoo Finance |
| `src/features.py` | Calculates technical indicators |
| `src/model.py` | Defines LSTM architecture |
| `src/train.py` | Trains the model |
| `src/backtest.py` | Tests trading strategy |
| `app.py` | Streamlit web application |
| `predict.py` | Make predictions from command line |
| `config.py` | Configuration settings |
| `requirements.txt` | Python dependencies |

## 💡 Tips for Success

1. **Start with default settings** - Don't change anything initially
2. **Wait for training** - 5-10 minutes is normal
3. **Try different stocks** - See how model performs on various stocks
4. **Read the documentation** - README.md has detailed explanations
5. **Experiment** - Change parameters in config.py and see what happens

## ⚠️ Important Notes

### This is Educational
- NOT financial advice
- NOT guaranteed to make money
- For learning purposes only

### Stock Prediction is Hard
- Even 55% accuracy is good
- Markets are unpredictable
- Past performance ≠ future results

### Real Trading Requires
- Risk management
- Stop losses
- Position sizing
- Transaction cost consideration
- Emotional discipline

## 🚀 You're Ready!

You now have a complete stock prediction system:
- ✅ Data pipeline
- ✅ Feature engineering
- ✅ LSTM model
- ✅ Backtesting
- ✅ Web interface

**Have fun learning and experimenting!**

## 📞 Need Help?

1. Check [README.md](README.md)
2. Check [USAGE.md](USAGE.md)
3. Run `python test_project.py` to diagnose issues
4. Review error messages carefully

## 🎓 Learning Resources

### Understand LSTM
- [Understanding LSTM Networks](http://colah.github.io/posts/2015-08-Understanding-LSTMs/)

### Technical Indicators
- [Investopedia - Technical Indicators](https://www.investopedia.com/terms/t/technicalindicator.asp)

### Python for Finance
- [Python for Finance Book](https://www.oreilly.com/library/view/python-for-finance/9781492024323/)

### Machine Learning
- [TensorFlow Tutorials](https://www.tensorflow.org/tutorials)

---

**Happy Learning! 🎉**

Remember: This is a learning project. Always do your own research before making investment decisions!
