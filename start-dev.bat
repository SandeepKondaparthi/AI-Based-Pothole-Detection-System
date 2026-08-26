@echo off
echo ========================================
echo RoadCare Development Server Starter
echo ========================================
echo.

echo Starting Backend Server (FastAPI)...
start cmd /k "cd backend && .venv\Scripts\activate && python run.py"

timeout /t 3 /nobreak > nul

echo.
echo Starting Frontend Server (React + Vite)...
start cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo ========================================
echo.
echo Press any key to exit...
pause > nul
