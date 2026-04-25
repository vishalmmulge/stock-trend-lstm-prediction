# Screenshots Guide

## What to Capture

Take these screenshots when running your Streamlit app:

### 1. Main Dashboard (main_dashboard.png)
- Show the app title and configuration sidebar
- Display a stock ticker input (e.g., RELIANCE.NS)
- Capture the prediction section with UP/DOWN trend
- Include confidence percentage

### 2. Technical Indicators (technical_indicators.png)
- Capture the charts showing:
  - SMA (20 and 50)
  - RSI with overbought/oversold lines
  - MACD with signal line

### 3. Backtest Results (backtest_results.png)
- Show the performance metrics:
  - Strategy Return
  - Buy & Hold Return
  - Portfolio value chart
  - Final portfolio value

### 4. Swing Trading Recommendation (swing_trading.png)
- Capture the recommendation section:
  - Buy/Sell/Hold signal
  - Signal strength
  - Price targets
  - Stop loss levels

## How to Take Screenshots

### Windows:
1. **Snipping Tool**: Search for "Snipping Tool" in Start menu
2. **Snip & Sketch**: Press `Win + Shift + S`
3. **Full Screen**: Press `PrtScn` (Print Screen)

### Tips for Good Screenshots:
- Use full browser width for better visibility
- Zoom to 100% (Ctrl + 0)
- Hide unnecessary browser toolbars
- Use light theme for better readability
- Capture actual predictions with real data

## File Naming Convention

Save your screenshots as:
- `main_dashboard.png`
- `technical_indicators.png`
- `backtest_results.png`
- `swing_trading.png`
- `demo.gif` (optional: screen recording)

## Adding Screenshots to README

Once you have screenshots, add them to your README.md:

```markdown
## 📸 Screenshots

### Main Dashboard
![Main Dashboard](screenshots/main_dashboard.png)

### Technical Indicators
![Technical Indicators](screenshots/technical_indicators.png)

### Backtest Results
![Backtest Results](screenshots/backtest_results.png)
```

## Creating a Demo GIF (Optional)

1. Download **ScreenToGif**: https://www.screentogif.com/
2. Record 10-15 seconds of:
   - Entering a stock ticker
   - Clicking "Load & Predict"
   - Scrolling through results
3. Save as `demo.gif`
4. Add to README:
   ```markdown
   ## 🎬 Demo
   ![Demo](screenshots/demo.gif)
   ```

## After Adding Screenshots

```bash
git add screenshots/
git commit -m "Add project screenshots for documentation"
git push
```

Your GitHub repository will now have visual examples of your project! 🎉
