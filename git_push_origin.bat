@echo off
echo ========================================
echo Git Push Script for Ada v2
echo Pushing to origin (nazirlouis/ada_v2)
echo ========================================
echo.

cd /d E:\jarvis\ada_v2

echo Current remotes:
git remote -v
echo.

echo Checking git status...
git status
echo.

echo Staging all changes...
git add .
echo.

echo Creating commit...
git commit -m "Enhanced Ada v2: Increased memory to 100 msgs, fixed face auth for Windows, completed Hue integration" || echo "Nothing to commit or commit failed"
echo.

echo Pushing to origin/main (nazirlouis/ada_v2)...
git push origin main
echo.

echo ========================================
echo Done! Check output above for any errors
echo ========================================
pause
