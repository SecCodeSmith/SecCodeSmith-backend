#!/bin/bash

# SecCodeSmith Backend - Development Commands for Linux/macOS

set -e

show_help() {
    echo "SecCodeSmith Backend Development Script"
    echo ""
    echo "Usage: ./dev.sh [command]"
    echo ""
    echo "Available commands:"
    echo "  help         - Show this help message"
    echo "  install      - Install production dependencies"
    echo "  install-dev  - Install development dependencies"
    echo "  test         - Run tests"
    echo "  test-verbose - Run tests with verbose output"
    echo "  test-cov     - Run tests with coverage"
    echo "  lint         - Run linting checks"
    echo "  format       - Format code with black and isort"
    echo "  security     - Run security checks"
    echo "  quality      - Run all quality checks"
    echo "  migrate      - Run database migrations"
    echo "  makemigrations - Create new migrations"
    echo "  runserver    - Start development server"
    echo "  collectstatic - Collect static files"
    echo "  superuser    - Create superuser"
    echo "  shell        - Open Django shell"
    echo "  clean        - Clean cached files"
    echo "  setup        - Setup development environment"
    echo "  docker-build - Build Docker image"
    echo "  docker-run   - Run Docker container"
    echo "  ci           - Run CI pipeline locally"
    echo ""
}

install_deps() {
    echo "📦 Installing production dependencies..."
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Production dependencies installed!"
}

install_dev_deps() {
    echo "📦 Installing development dependencies..."
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Development dependencies installed!"
}

run_tests() {
    echo "🧪 Running tests..."
    pytest
}

run_tests_verbose() {
    echo "🧪 Running tests with verbose output..."
    pytest -v
}

run_tests_coverage() {
    echo "🧪 Running tests with coverage..."
    pytest --cov=. --cov-report=html --cov-report=term
    echo "📊 Coverage report generated in htmlcov/"
}

run_lint() {
    echo "🔍 Running linting checks..."
    echo "  - flake8..."
    flake8 .
    echo "  - black check..."
    black --check .
    echo "  - isort check..."
    isort --check-only .
    echo "✅ All linting checks passed!"
}

format_code() {
    echo "🎨 Formatting code..."
    echo "  - Running black..."
    black .
    echo "  - Running isort..."
    isort .
    echo "✅ Code formatted!"
}

run_security() {
    echo "🛡️ Running security checks..."
    echo "  - bandit..."
    bandit -r .
    echo "  - safety..."
    safety check
    echo "✅ Security checks completed!"
}

run_quality_checks() {
    echo "🔍 Running all quality checks..."
    run_lint
    run_security
    echo "✅ All quality checks completed!"
}

run_migrations() {
    echo "🗃️ Running database migrations..."
    python manage.py migrate
    echo "✅ Migrations completed!"
}

make_migrations() {
    echo "🗃️ Creating new migrations..."
    python manage.py makemigrations
    echo "✅ Migrations created!"
}

run_server() {
    echo "🚀 Starting development server..."
    python manage.py runserver
}

collect_static() {
    echo "📁 Collecting static files..."
    python manage.py collectstatic --noinput
    echo "✅ Static files collected!"
}

create_superuser() {
    echo "👤 Creating superuser..."
    python manage.py createsuperuser
}

open_shell() {
    echo "🐍 Opening Django shell..."
    python manage.py shell
}

clean_cache() {
    echo "🧹 Cleaning cached files..."
    find . -type f -name "*.pyc" -delete
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
    rm -rf .pytest_cache
    rm -rf .coverage
    rm -rf htmlcov/
    echo "✅ Cache cleaned!"
}

setup_dev() {
    echo "🛠️ Setting up development environment..."
    install_dev_deps
    run_migrations
    echo "✅ Development environment ready!"
}

build_docker() {
    echo "🐳 Building Docker image..."
    docker build -t seccodesmithbackend:latest .
    echo "✅ Docker image built!"
}

run_docker() {
    echo "🐳 Running Docker container..."
    docker run -p 8000:8000 seccodesmithbackend:latest
}

run_ci() {
    echo "🔄 Running CI pipeline locally..."
    run_tests_coverage
    run_quality_checks
    echo "✅ CI pipeline completed!"
}

# Main script logic
case "${1:-help}" in
    help)
        show_help
        ;;
    install)
        install_deps
        ;;
    install-dev)
        install_dev_deps
        ;;
    test)
        run_tests
        ;;
    test-verbose)
        run_tests_verbose
        ;;
    test-cov)
        run_tests_coverage
        ;;
    lint)
        run_lint
        ;;
    format)
        format_code
        ;;
    security)
        run_security
        ;;
    quality)
        run_quality_checks
        ;;
    migrate)
        run_migrations
        ;;
    makemigrations)
        make_migrations
        ;;
    runserver)
        run_server
        ;;
    collectstatic)
        collect_static
        ;;
    superuser)
        create_superuser
        ;;
    shell)
        open_shell
        ;;
    clean)
        clean_cache
        ;;
    setup)
        setup_dev
        ;;
    docker-build)
        build_docker
        ;;
    docker-run)
        run_docker
        ;;
    ci)
        run_ci
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
