@echo off
setlocal
TITLE Antigravity Skills App

echo ===================================================
echo      Antigravity Awesome Skills - Web App
echo ===================================================

:: Check for Node.js
WHERE node >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed. Please install it from https://nodejs.org/
    pause
    exit /b 1
)

:: ===== Auto-Update Skills from GitHub =====
echo [INFO] Checking for skill updates...

:: Method 1: Try Git first (if available)
WHERE git >nul 2>nul
IF %ERRORLEVEL% EQU 0 goto :USE_GIT

:: Method 2: Try PowerShell download (fallback)
echo [INFO] Git not found. Using alternative download method...
goto :USE_POWERSHELL

:USE_GIT
:: Add upstream remote if not already set
git remote get-url upstream >nul 2>nul
IF %ERRORLEVEL% EQU 0 goto :DO_FETCH
echo [INFO] Adding upstream remote...
git remote add upstream https://github.com/sickn33/antigravity-awesome-skills.git

:DO_FETCH
echo [INFO] Fetching latest skills from original repo...
git fetch upstream >nul 2>nul
IF %ERRORLEVEL% NEQ 0 goto :FETCH_FAIL
goto :DO_MERGE

:FETCH_FAIL
echo [WARN] Could not fetch updates via Git. Trying alternative method...
goto :USE_POWERSHELL

:DO_MERGE
:: Surgically extract ONLY the /skills/ folder from upstream to avoid all merge conflicts
git checkout upstream/main -- skills >nul 2>nul
IF %ERRORLEVEL% NEQ 0 goto :MERGE_FAIL

:: Save the updated skills to local history silently
git commit -m "auto-update: sync latest skills from upstream" >nul 2>nul
echo [INFO] Skills updated successfully from original repo!
goto :SKIP_UPDATE

:MERGE_FAIL
echo [WARN] Could not update skills via Git. Trying alternative method...
goto :USE_POWERSHELL

:USE_POWERSHELL
echo [INFO] Downloading latest skills via HTTPS...
if exist "update_temp" rmdir /S /Q "update_temp" >nul 2>nul
if exist "update.zip" del "update.zip" >nul 2>nul

:: Download the latest repository as ZIP
powershell -Command "Invoke-WebRequest -Uri 'https://github.com/sickn33/antigravity-awesome-skills/archive/refs/heads/main.zip' -OutFile 'update.zip' -UseBasicParsing" >nul 2>nul
IF %ERRORLEVEL% NEQ 0 goto :DOWNLOAD_FAIL

:: Extract and update skills
echo [INFO] Extracting latest skills...
powershell -Command "Expand-Archive -Path 'update.zip' -DestinationPath 'update_temp' -Force" >nul 2>nul
IF %ERRORLEVEL% NEQ 0 goto :EXTRACT_FAIL

:: Copy only the skills folder
if exist "update_temp\antigravity-awesome-skills-main\skills" (
    echo [INFO] Updating skills directory...
    xcopy /E /Y /I "update_temp\antigravity-awesome-skills-main\skills" "skills" >nul 2>nul
    echo [INFO] Skills updated successfully without Git!
) else (
    echo [WARN] Could not find skills folder in downloaded archive.
    goto :UPDATE_FAIL
)

:: Cleanup
del "update.zip" >nul 2>nul
rmdir /S /Q "update_temp" >nul 2>nul
goto :SKIP_UPDATE

:DOWNLOAD_FAIL
echo [WARN] Failed to download skills update (network issue or no internet).
goto :UPDATE_FAIL

:EXTRACT_FAIL
echo [WARN] Failed to extract downloaded skills archive.
goto :UPDATE_FAIL

:UPDATE_FAIL
echo [INFO] Continuing with local skills version...
echo [INFO] To manually update skills later, run: npm run update:skills

:SKIP_UPDATE

:: Check/Install dependencies
cd web-app

:CHECK_DEPS
if not exist "node_modules\" (
    echo [INFO] Dependencies not found. Installing...
    goto :INSTALL_DEPS
)

:: Verify dependencies aren't corrupted (e.g. esbuild arch mismatch after update)
echo [INFO] Verifying app dependencies...
call npx -y vite --version >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [WARN] Dependencies appear corrupted or outdated.
    echo [INFO] Cleaning up and reinstalling fresh dependencies...
    rmdir /s /q "node_modules" >nul 2>nul
    goto :INSTALL_DEPS
)
goto :DEPS_OK

:INSTALL_DEPS
call npm install
call npm install @supabase/supabase-js
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install dependencies. Please check your internet connection.
    pause
    exit /b 1
)

:DEPS_OK
cd ..

:: Run setup script
echo [INFO] Updating skills data...
call npm run app:setup

:: Start App
echo [INFO] Starting Web App...
echo [INFO] Opening default browser...
cd web-app
call npx -y vite --open

endlocal
