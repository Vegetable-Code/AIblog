@echo off
cd /d E:\projects\blog

echo [1/3] Starting Backend...
start "Blog-Backend" cmd /c "D:\Anaconda\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
timeout /t 3 /nobreak >nul

echo [2/3] Starting Frontend...
start "Blog-Frontend" cmd /c "D:\Node\npx.cmd vite --host 0.0.0.0 --port 3000"
timeout /t 3 /nobreak >nul

echo [3/3] Starting Admin...
start "Blog-Admin" cmd /c "D:\Node\npx.cmd vite --host 0.0.0.0 --port 3001"
timeout /t 3 /nobreak >nul

echo.
echo ====================================
echo  All services started!
echo  Frontend: http://localhost:3000
echo  Admin:    http://localhost:3001
echo  API:      http://localhost:8000
echo ====================================
echo.
pause
