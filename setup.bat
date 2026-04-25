@echo off
echo ============================================================
echo Stock Trend Prediction - Setup Script
echo ============================================================
echo.

echo [1/4] Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error creating virtual environment!
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo [3/4] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing dependencies!
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo [4/4] Running tests...
python test_project.py
echo.

echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo 1. Run: python quick_start.py
echo 2. Or run: python -m src.train
echo 3. Then: streamlit run app.py
echo.
pause
