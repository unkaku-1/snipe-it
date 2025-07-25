@echo off
setlocal

:: ============================================================================
:: Snipe-IT Fixed Deployment Script (Windows)
::
:: This script provides multiple deployment options:
:: 1. Official pre-built image (recommended)
:: 2. Custom build with network fixes (for China users)
:: 3. Original custom build (fallback)
:: ============================================================================

echo.
echo ==========================================
echo   Snipe-IT Fixed Deployment Script
echo ==========================================
echo.

:: --- Environment Checks ---
echo [1/6] Checking environment...

:check_git
echo      - Checking for Git...
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo      ERROR: Git not found. Please install Git and ensure it's in your system's PATH.
    goto :eof
)
echo      - Git is installed.

:check_docker
echo      - Checking for Docker...
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo      ERROR: Docker not found. Please install Docker Desktop.
    goto :eof
)
echo      - Docker is installed.

:check_docker_running
echo      - Checking Docker service status...
docker info >nul 2>nul
if %errorlevel% neq 0 (
    echo      ERROR: Docker Desktop is not running or not responding.
    echo      Please start Docker Desktop and ensure it's in Linux container mode.
    goto :eof
)
echo      - Docker service is running.
echo.

:: --- Deployment Method Selection ---
echo [2/6] Select deployment method:
echo.
echo   1. Official pre-built image (Recommended - fastest, most stable)
echo   2. Custom build with network fixes (For users in China or with network issues)
echo   3. Original custom build (Fallback option)
echo.
set /p choice="Please enter your choice (1-3): "

if "%choice%"=="1" (
    set compose_file=docker-compose.official.yml
    echo      - Selected: Official pre-built image
) else if "%choice%"=="2" (
    set compose_file=docker-compose.fixed.yml
    echo      - Selected: Custom build with network fixes
) else if "%choice%"=="3" (
    set compose_file=docker-compose.yml
    echo      - Selected: Original custom build
) else (
    echo      ERROR: Invalid choice. Please run the script again and select 1, 2, or 3.
    goto :eof
)
echo.

:: --- Create .env file ---
echo [3/6] Checking for .env configuration file...
if exist .env (
    echo      - .env file already exists. Skipping creation.
) else (
    echo      - .env file not found. Creating it for you...
    (
        echo # Auto-generated by deploy_snipeit_fixed.bat for local Docker environment
        echo APP_ENV=development
        echo APP_DEBUG=true
        echo APP_KEY=base64:tQp/IFsfrhK5eLh3kI/y0Ie2Ld5pA9aT7CqLdI3iJcE=
        echo APP_URL=http://localhost:8000
        echo APP_TIMEZONE='UTC'
        echo APP_LOCALE='zh-CN'
        echo APP_VERSION=latest
        echo.
        echo DB_CONNECTION=mysql
        echo DB_HOST=db
        echo DB_PORT=3306
        echo DB_DATABASE=snipeit
        echo DB_USERNAME=snipeit
        echo DB_PASSWORD=snipeit
        echo MYSQL_ROOT_PASSWORD=snipeit_root_password
        echo.
        echo MAIL_MAILER=log
        echo MAIL_HOST=localhost
        echo MAIL_PORT=1025
        echo MAIL_USERNAME=null
        echo MAIL_PASSWORD=null
        echo MAIL_FROM_ADDR=deploy_script@example.com
        echo MAIL_FROM_NAME='Snipe-IT'
        echo MAIL_REPLYTO_ADDR=deploy_script@example.com
        echo.
        echo IMAGE_LIB=gd
    ) > .env
    echo      - .env file created successfully.
)
echo.

:: --- Stop existing services ---
echo [4/6] Stopping any existing services...
docker-compose -f %compose_file% down >nul 2>nul
echo      - Existing services stopped.
echo.

:: --- Start Docker Services ---
echo [5/6] Building and starting services with Docker Compose...
echo      Using configuration file: %compose_file%
echo      This may take a long time, especially on the first run. Please be patient.
docker-compose -f %compose_file% up -d --build
if %errorlevel% neq 0 (
    echo.
    echo      ERROR: Docker Compose failed to build or start!
    echo      Please check the Docker logs for detailed error messages.
    echo.
    echo      Common solutions:
    echo      1. Check your internet connection
    echo      2. Try running the script again with option 2 (network fixes)
    echo      3. Check Docker Desktop settings and ensure Linux containers are enabled
    echo      4. Restart Docker Desktop and try again
    goto :eof
)
echo      - Docker services started successfully.
echo.

:: --- Clear Config Cache (only for custom builds) ---
if not "%choice%"=="1" (
    echo [6/6] Clearing application config cache...
    timeout /t 10 /nobreak >nul
    docker-compose -f %compose_file% exec app php artisan config:clear
    if %errorlevel% neq 0 (
        echo.
        echo      WARNING: Failed to clear config cache. The app might not load the latest settings.
        echo      You can try running 'docker-compose -f %compose_file% exec app php artisan config:clear' manually later.
    ) else (
        echo      - Config cache cleared successfully.
    )
) else (
    echo [6/6] Skipping cache clear for official image...
)
echo.

:: --- Done ---
echo =====================================================
echo          DEPLOYMENT SUCCESSFUL
echo =====================================================
echo.
echo You can now access Snipe-IT at:
echo.
echo   - Snipe-IT Application: http://localhost:8000
echo.
echo Configuration used: %compose_file%
echo.
echo On your first visit, follow the "Pre-Flight Check" instructions to complete the setup.
echo.
echo Useful commands:
echo   - View logs: docker-compose -f %compose_file% logs -f
echo   - Stop services: docker-compose -f %compose_file% down
echo   - Restart services: docker-compose -f %compose_file% restart
echo.

endlocal
pause

