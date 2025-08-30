# SecCodeSmith Backend - Development Commands

.PHONY: help install install-dev test test-verbose lint format security clean migrate runserver docker-build docker-run

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install --upgrade pip
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test: ## Run tests
	pytest

test-verbose: ## Run tests with verbose output
	pytest -v

test-coverage: ## Run tests with coverage report
	pytest --cov=. --cov-report=html --cov-report=term

lint: ## Run all linting checks
	flake8 .
	black --check .
	isort --check-only .

format: ## Format code with black and isort
	black .
	isort .

security: ## Run security checks
	bandit -r .
	safety check

quality: lint security ## Run all quality checks

clean: ## Clean up cached files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov/

migrate: ## Run database migrations
	python manage.py migrate

makemigrations: ## Create new migrations
	python manage.py makemigrations

runserver: ## Start development server
	python manage.py runserver

collectstatic: ## Collect static files
	python manage.py collectstatic --noinput

superuser: ## Create superuser
	python manage.py createsuperuser

shell: ## Open Django shell
	python manage.py shell

docker-build: ## Build Docker image
	docker build -t seccodesmithbackend:latest .

docker-run: ## Run Docker container
	docker run -p 8000:8000 seccodesmithbackend:latest

docker-compose-up: ## Start all services with docker-compose
	docker-compose up -d

docker-compose-down: ## Stop all services
	docker-compose down

all-checks: test lint security ## Run all checks (tests, linting, security)

setup: install-dev migrate ## Setup development environment

ci: all-checks ## Run CI pipeline locally
