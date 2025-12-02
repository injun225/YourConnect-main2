@echo off
title 🚀 YourConnect Development Environment

echo ==========================================
echo     🚀 Starting YourConnect Environment
echo ==========================================

cd /d "C:\Users\user\YourConnectDB\career_platform"

echo [1/3] 🧠 Activating virtual environment...
call .\venv\Scripts\activate

echo [2/3] 🔌 Starting Redis server...
start "Redis Server" cmd /k "redis-server"

echo [3/3] ⚙️ Starting Celery worker...
start "Celery Worker" cmd /k "cd /d C:\Users\user\YourConnectDB\career_platform && .\venv\Scripts\activate && celery -A career_platform worker -l info --pool=solo"

echo 🌐 Starting Django server...
start "Django Server" cmd /k "cd /d C:\Users\user\YourConnectDB\career_platform && .\venv\Scripts\activate && python manage.py runserver"

echo ✅ All services started successfully!
pause
