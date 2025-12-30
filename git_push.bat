@echo off
echo ========================================
echo Git Push Script for Ada v2
echo ========================================
echo.

cd /d E:\jarvis\ada_v2

echo Checking git status...
git status
echo.

echo Checking current remote...
git remote -v
echo.

echo Adding andreransom58-coder remote if not exists...
git remote get-url andreransom58-coder >nul 2>&1
if errorlevel 1 (
    echo Remote not found, adding it...
    git remote add andreransom58-coder https://github.com/andreransom58-coder/ada_v2.git
) else (
    echo Remote already exists
)
echo.

echo Fetching from remote...
git fetch andreransom58-coder
echo.

echo Staging all changes...
git add .
echo.

echo Creating commit...
git commit -m "Enhanced Ada v2: Increased memory to 100 msgs, fixed face auth for Windows, completed Hue integration"
echo.

echo Pushing to GitHub (andreransom58-coder/ada_v2)...
git push andreransom58-coder main
echo.

echo ========================================
echo Done! Check output above for any errors
echo ========================================
pause
