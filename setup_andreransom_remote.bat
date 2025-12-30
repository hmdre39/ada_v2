@echo off
echo Updating andreransom58-coder remote URL...
cd /d E:\jarvis\ada_v2

echo Enter the repository name on GitHub (without https://github.com/andreransom58-coder/):
set /p REPO_NAME=

git remote remove andreransom58-coder 2>nul
git remote add andreransom58-coder https://github.com/andreransom58-coder/%REPO_NAME%.git

echo.
echo Remote updated! Now pushing...
git push andreransom58-coder main

pause
