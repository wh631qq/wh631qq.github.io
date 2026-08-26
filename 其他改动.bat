@echo off
cd /d "%~dp0"
git add -A
git diff --cached --quiet
if errorlevel 1 (
  git commit -m "update other changes"
  git push
  echo Done. Pushed.
) else (
  echo Nothing to commit.
)
echo.
pause
