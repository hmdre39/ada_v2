@echo off
echo ========================================
echo Git Push Script for Ada v2
echo Pushing to hmdre39/ada_v2
echo ========================================
echo.

cd /d E:\jarvis\ada_v2

echo Checking git status...
git status
echo.

echo Current remotes:
git remote -v
echo.

echo Checking if hmdre39 remote exists...
git remote get-url hmdre39 >nul 2>&1
if errorlevel 1 (
    echo Adding hmdre39 remote...
    git remote add hmdre39 https://github.com/hmdre39/ada_v2.git
) else (
    echo Updating hmdre39 remote URL...
    git remote set-url hmdre39 https://github.com/hmdre39/ada_v2.git
)
echo.

echo Fetching from hmdre39...
git fetch hmdre39 2>nul || echo "Note: Repository may not exist yet on GitHub"
echo.

echo Staging all changes...
git add .
echo.

echo Creating commit with today's changes...
git commit -m "Enhanced Ada v2: Memory system upgrade, Face auth Windows fix, Hue integration

- Increased long-term memory from 10 to 100 messages (configurable up to 200)
- Added memory_context_limit and max_memory_file_size_mb settings
- Fixed face authentication camera initialization for Windows (was macOS only)
- Added platform detection for camera API (Windows/macOS/Linux)
- Created diagnostic tools: check_auth.py and capture_reference.py
- Completed Philips Hue smart lighting integration (95%% complete)
- Added discover_hue and control_hue Socket.IO endpoints
- Integrated HueAgent with voice commands and AudioLoop
- Updated settings.json with new configuration options" || echo "Nothing new to commit"
echo.

echo Pushing to hmdre39/main...
git push hmdre39 main
if errorlevel 1 (
    echo.
    echo Push failed. Trying force push...
    echo WARNING: This will overwrite remote history!
    choice /C YN /M "Do you want to force push"
    if errorlevel 2 goto :skip_force
    git push -f hmdre39 main
    :skip_force
)
echo.

echo ========================================
echo Done! Check output above for any errors
echo ========================================
echo.
echo Repository should be at: https://github.com/hmdre39/ada_v2
echo.
pause
