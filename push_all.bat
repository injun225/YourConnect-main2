@echo off
cd /d "C:\Users\user\YourConnectDB\career_platform"

echo 🔄 Activating virtual environment...
call .\venv\Scripts\activate

echo 📁 Checking git status...
git status

echo 🧩 Staging all changes...
git add .

set /p msg=💬 Commit message 입력하세요: 
if "%msg%"=="" set msg=update auto commit

echo 💾 Committing changes...
git commit -m "%msg%"

echo ⬇️ Pulling latest changes from remote...
git pull origin main --rebase

echo ⬆️ Pushing to GitHub...
git push origin main

echo ✅ 작업 완료! GitHub에 최신 코드가 업로드되었습니다.
pause


