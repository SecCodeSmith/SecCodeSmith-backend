# SecCodeSmith Backend

[![CI/CD Pipeline](https://github.com/SecCodeSmith/SecCodeSmith-backend/actions/workflows/ci.yml/badge.svg)](https://github.com/SecCodeSmith/SecCodeSmith-backend/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Django 5.2+](https://img.shields.io/badge/django-5.2+-green.svg)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.16+-red.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-15+-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/redis-7+-red.svg)](https://redis.io/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![codecov](https://codecov.io/gh/SecCodeSmith/SecCodeSmith-backend/branch/main/graph/badge.svg)](https://codecov.io/gh/SecCodeSmith/SecCodeSmith-backend)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

This repository contains the Django-powered REST API backend for the SecCodeSmith portfolio website. It provides endpoints for blog posts, project showcases, image properties, and static page content (About, Contact, Skills, Footer Links).

## Table of Contents

* [About](#about)
* [Features](#features)
* [Tech Stack](#tech-stack)
* [Requirements](#requirements)
* [Quick Start](#quick-start)
* [Installation](#installation)
* [Configuration](#configuration)
* [Running the Server](#running-the-server)
* [Testing](#testing)
* [Code Quality](#code-quality)
* [Docker Support](#docker-support)
* [API Reference](#api-reference)
  * [General API](#general-api)
  * [Blog API](#blog-api)
  * [Project API](#project-api)
  * [Images API](#images-api)
* [Contributing](#contributing)
* [CI/CD Pipeline](#cicd-pipeline)
* [License](#license)
* [Contact](#contact)

---

## About

SecCodeSmith Backend serves as the data layer for the portfolio site, supplying JSON over REST endpoints that the front-end consumes for dynamic content. The API is built with Django and Django REST Framework, providing a robust and scalable foundation for the portfolio website.

---

## Features

* **🔥 Blog Posts**: List, paginate, and count pages of blog entries
* **🚀 Project Showcase**: List projects, view details, and filter by category
* **🖼️ Image Properties**: Serve metadata for portfolio images
* **📄 Static Pages**: Endpoints for About, Contact, Skills, and Footer Links content
* **🔒 CSRF Support**: Retrieve CSRF tokens for secure front-end forms
* **👨‍💼 Admin Interface**: Built-in Django admin at `/admin/`
* **🧪 Comprehensive Testing**: Unit tests with pytest and Django TestCase
* **🔍 Code Quality**: Automated linting, formatting, and security checks
* **🐳 Docker Support**: Containerized deployment ready
* **⚡ Caching**: Redis-based caching for improved performance

---

## Tech Stack

* **🐍 Python** 3.10+
* **🌐 Django** 5.2.1
* **📡 Django REST Framework** 3.16.0
* **🗃️ PostgreSQL** (Production) / SQLite (Development)
* **🔴 Redis** for caching
* **🧪 pytest** for testing
* **🔍 flake8, black, isort** for code quality
* **🛡️ bandit, safety** for security scanning
* **🐳 Docker** for containerization

---

## Requirements

* Python 3.10 or later
* pip (Python package installer)
* Redis (for caching)
* PostgreSQL (optional, for production)

---

## Quick Start

Get up and running in less than 5 minutes:

**Linux/macOS:**
```bash
# Clone the repository
git clone https://github.com/SecCodeSmith/SecCodeSmith-backend.git
cd SecCodeSmith-backend

# Make script executable and setup
chmod +x dev.sh
./dev.sh setup

# Start the server
./dev.sh runserver
```

**Windows:**
```cmd
# Clone the repository
git clone https://github.com/SecCodeSmith/SecCodeSmith-backend.git
cd SecCodeSmith-backend

# Setup environment
dev.bat setup

# Start the server
dev.bat runserver
```

**Using Make (Linux/macOS):**
```bash
# Setup development environment
make setup

# Start the server
make runserver
```

The API will be available at `http://127.0.0.1:8000/`

### 🎯 Development Scripts

This project includes convenient development scripts:

- **Linux/macOS**: `./dev.sh [command]`
- **Windows**: `dev.bat [command]`
- **Make**: `make [target]` (Linux/macOS only)

Available commands:
- `setup` - Complete development environment setup
- `test` - Run test suite
- `lint` - Run code quality checks
- `format` - Format code with black and isort
- `runserver` - Start Django development server
- `migrate` - Run database migrations
- `security` - Run security scans

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/SecCodeSmith/SecCodeSmith-backend.git
cd SecCodeSmith-backend
```

### 2. Set Up Virtual Environment

**Linux/macOS:**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set Up Environment Variables (Optional)

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your_super_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Optional - defaults to SQLite)
DATABASE_TYPE=sqlite  # or 'pgsql' for PostgreSQL
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=seccodesmithbackend

# Redis (Optional - uses fakeredis for development)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Email (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_USE_TLS=True
EMAIL_SMTP_PORT=587
```

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

---

## Configuration

The project uses environment variables for configuration via `django-environ`. Create a `.env` file to override default settings:

### Database Configuration

**SQLite (Default - Development):**
```env
DATABASE_TYPE=sqlite
```

**PostgreSQL (Production):**
```env
DATABASE_TYPE=pgsql
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=seccodesmithbackend
```

### Caching Configuration

**Development (FakeRedis):**
No configuration needed - uses in-memory caching.

**Production (Redis):**
```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=your_redis_password
```

---

## Running the Server

### Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

### Available Endpoints

- **API Root**: `http://127.0.0.1:8000/api/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`
- **Blog API**: `http://127.0.0.1:8000/blog-api/`
- **Project API**: `http://127.0.0.1:8000/project-api/`
- **Images API**: `http://127.0.0.1:8000/img/`

---

## Testing

### Run All Tests

```bash
# Using pytest (recommended)
pytest

# Using Django test runner
python manage.py test
```

### Run Specific Tests

```bash
# Test specific app
pytest api/test.py

# Test specific test class
pytest api/test.py::SkillCardsViewTests

# Test with verbose output
pytest -v

# Test with coverage
pytest --cov=.
```

### Test Configuration

Tests are configured to use:
- In-memory SQLite database
- Local memory cache
- Isolated test environment

---

## Code Quality

This project maintains high code quality through automated tools:

### Linting and Formatting

```bash
# Check code style
flake8 .

# Format code
black .

# Sort imports
isort .

# Run all checks
flake8 . && black --check . && isort --check-only .
```

### Security Scanning

```bash
# Scan for security issues
bandit -r .

# Check for vulnerable dependencies
safety check
```

---

## Docker Support

### Build and Run with Docker

```bash
# Build the image
docker build -t seccodesmithbackend .

# Run the container
docker run -p 8000:8000 seccodesmithbackend
```

### Docker Compose (with PostgreSQL and Redis)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## VS Code Setup

This project is optimized for Visual Studio Code with comprehensive configuration:

### 🚀 Quick Setup

1. **Open the workspace**: Use `SecCodeSmith-backend.code-workspace`
2. **Install recommended extensions**: VS Code will prompt you automatically
3. **Select Python interpreter**: Choose `.venv/bin/python` when prompted

### 🔧 Pre-configured Features

- **Debugging**: Ready-to-use debug configurations for Django
- **Testing**: Integrated pytest runner with coverage
- **Linting**: Automated code quality checks
- **Formatting**: Auto-format on save with Black
- **Tasks**: One-click Django commands (F1 → "Tasks: Run Task")

### 📋 Available Debug Configurations

- `Django: Run Server` - Start development server with debugging
- `Django: Run Tests` - Run test suite with debugging
- `Django: Shell` - Open Django shell with debugging
- `Django: Migrate` - Run migrations
- `Django: Make Migrations` - Create new migrations

### ⚡ VS Code Tasks

Access via `Ctrl+Shift+P` → "Tasks: Run Task":
- Django: Run Server
- Django: Run Tests (with coverage)
- Code Quality: Lint/Format
- Security: Scan with Bandit
- Install Dependencies

---

## API Reference

### General API

Base path: `/api/`

| Endpoint            | Method | Description                            |
| ------------------- | ------ | -------------------------------------- |
| `/api/csrf`         | GET    | Retrieve CSRF token                    |
| `/api/skills-cards` | GET    | List skill cards for front-end display |
| `/api/about/`       | GET    | Get content for the “About” page       |
| `/api/footer-links` | GET    | List social/footer links               |
| `/api/contact/`     | GET    | Get content for the “Contact” page     |

---

### Blog API

Base path: `/blog-api/`

| Endpoint                        | Method | Description                              |
| ------------------------------- | ------ | ---------------------------------------- |
| `/blog-api/post/`               | GET    | List all blog posts                      |
| `/blog-api/count_pages/`        | GET    | Retrieve total number of paginated pages |
| `/blog-api/post-page/?page=<n>` | GET    | List posts on page `<n>`                 |

---

### Project API

Base path: `/project-api/`

| Endpoint                      | Method | Description                            |
| ----------------------------- | ------ | -------------------------------------- |
| `/project-api/projects/`      | GET    | List all projects                      |
| `/project-api/projects/<id>/` | GET    | Get details for project with ID `<id>` |
| `/project-api/cat`            | GET    | List available project categories      |

---

### Images API

Base path: `/img/`

| Endpoint           | Method | Description                                     |
| ------------------ | ------ | ----------------------------------------------- |
| `/img/Image/<id>/` | GET    | Retrieve properties (metadata) for image `<id>` |

---

## Contributing

We welcome contributions! Please follow these steps:

### 1. Fork and Clone

```bash
git clone https://github.com/your-username/SecCodeSmith-backend.git
cd SecCodeSmith-backend
```

### 2. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Set Up Development Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
```

### 4. Make Changes and Test

```bash
# Run tests
pytest

# Check code quality
flake8 .
black --check .
isort --check-only .

# Run security checks
bandit -r .
safety check
```

### 5. Commit and Push

```bash
git add .
git commit -m "Add your descriptive commit message"
git push origin feature/your-feature-name
```

### 6. Create Pull Request

Open a Pull Request on GitHub with:
- Clear description of changes
- Reference to any related issues
- Screenshots if applicable

### Code Style Guidelines

- Follow PEP 8 (enforced by flake8)
- Use Black for code formatting
- Sort imports with isort
- Write comprehensive tests for new features
- Add docstrings for complex functions
- Keep line length under 127 characters

---

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment:

### Automated Checks

Every push and pull request triggers:

**🧪 Testing Pipeline:**
- Tests on Python 3.10, 3.11, and 3.12
- PostgreSQL and Redis service containers
- Full test suite execution with pytest
- Django system checks
- Code coverage reporting with Codecov

**🔍 Code Quality Pipeline:**
- Linting with flake8
- Code formatting check with black
- Import sorting check with isort

**🛡️ Security Pipeline:**
- Security vulnerability scanning with bandit
- Dependency vulnerability check with safety
- Semgrep static analysis

**🤖 AI-Powered Review Pipeline:**
- GitHub Copilot code review on PRs
- Automated code suggestions and improvements
- Django-specific best practices analysis
- Performance optimization recommendations
- Type checking with mypy

**🐳 Docker Pipeline:**
- Docker image build and test (on main branch)

### Status Badges

The README includes badges showing:
- ✅ CI/CD pipeline status
- 🐍 Python version compatibility
- 🌐 Django version
- 📜 License information
- 📊 Code coverage percentage

### Automated Code Review

- **🤖 GitHub Copilot**: Automated code review for PRs
- **💡 AI Suggestions**: Performance and best practices recommendations
- **🔍 Code Analysis**: Static analysis with pylint, mypy, and vulture
- **🛡️ Security Scanning**: Comprehensive security analysis

### Branch Protection

- `main` and `develop` branches require:
  - Passing CI checks
  - Code review approval
  - Up-to-date branches

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Contact

- **Project Repository**: [SecCodeSmith-backend](https://github.com/SecCodeSmith/SecCodeSmith-backend)
- **Organization**: [SecCodeSmith](https://github.com/SecCodeSmith)
- **Issues**: [Report a Bug](https://github.com/SecCodeSmith/SecCodeSmith-backend/issues)
- **Discussions**: [GitHub Discussions](https://github.com/SecCodeSmith/SecCodeSmith-backend/discussions)

---

## Acknowledgments

- Built with [Django](https://www.djangoproject.com/) and [Django REST Framework](https://www.django-rest-framework.org/)
- Testing powered by [pytest](https://pytest.org/)
- Code quality ensured by [Black](https://black.readthedocs.io/), [flake8](https://flake8.pycqa.org/), and [isort](https://pycqa.github.io/isort/)
- Security scanning by [Bandit](https://bandit.readthedocs.io/) and [Safety](https://pyup.io/safety/)
- CI/CD powered by [GitHub Actions](https://github.com/features/actions)
