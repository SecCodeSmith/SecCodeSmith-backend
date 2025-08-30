@echo off
REM SecCodeSmith Backend - Development Commands for Windows

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="install" goto install
if "%1"=="install-dev" goto install-dev
if "%1"=="test" goto test
if "%1"=="test-verbose" goto test-verbose
if "%1"=="lint" goto lint
if "%1"=="format" goto format
if "%1"=="security" goto security
if "%1"=="migrate" goto migrate
if "%1"=="runserver" goto runserver
if "%1"=="clean" goto clean
goto help

:help
echo Available commands:
echo   help         - Show this help message
echo   install      - Install production dependencies
echo   install-dev  - Install development dependencies
echo   test         - Run tests
echo   test-verbose - Run tests with verbose output
echo   lint         - Run linting checks
echo   format       - Format code
echo   security     - Run security checks
echo   migrate      - Run database migrations
echo   runserver    - Start development server
echo   clean        - Clean cached files
goto end

:install
pip install --upgrade pip
pip install -r requirements.txt
goto end

:install-dev
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
goto end

:test
pytest
goto end

:test-verbose
pytest -v
goto end

:lint
flake8 .
black --check .
isort --check-only .
goto end

:format
black .
isort .
goto end

:security
bandit -r .
safety check
goto end

:migrate
python manage.py migrate
goto end

:runserver
python manage.py runserver
goto end

:clean
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
if exist .pytest_cache rd /s /q .pytest_cache
if exist htmlcov rd /s /q htmlcov
goto end

:end
