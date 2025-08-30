# 🚀 CI/CD Pipeline Documentation

This directory contains GitHub Actions workflows for automated testing, building, and deployment of the SecCodeSmith Backend API.

## 📋 Available Workflows

### 1. Main CI/CD Pipeline (`.github/workflows/ci.yml`)

**Triggers**: Push to `main`, `develop`, feature branches, PRs to `main`/`develop`

**Features**:
- ✅ Multi-Python version testing (3.10, 3.11, 3.12)
- 🏗️ PostgreSQL and Redis service containers
- 🔍 Code quality checks (flake8, black, isort)
- 🛡️ Security scanning (bandit, safety)
- 🐳 Docker image testing (on main branch)
- 📊 Comprehensive test coverage

### 2. Pull Request Checks (`.github/workflows/pr.yml`)

**Triggers**: Pull requests to `main`, `develop`

**Features**:
- 🧪 Automated testing with detailed coverage reports
- 💬 Automatic PR comments with test results
- 📊 Coverage reporting with Codecov integration
- 🔍 Code quality validation
- 🛡️ Security vulnerability scanning
- ✅ Multi-Python version compatibility testing

### 3. Release Pipeline (`.github/workflows/release.yml`)

**Triggers**: Manual dispatch, Git tags (`v*`)

**Features**:
- 🔖 Automated version management
- 📝 Changelog generation from git commits
- 📦 Build artifacts (tar.gz, zip)
- 🐳 Docker image generation
- 📋 Release notes creation
- 🚀 GitHub Pages documentation deployment
- 🎯 Production-ready builds

### 4. Pre-release Pipeline (`.github/workflows/pre-release.yml`)

**Triggers**: Push to `develop`, feature branches, manual dispatch

**Features**:
- 🧪 Development branch testing
- 📅 Timestamp-based versioning
- 🧹 Automatic cleanup of old pre-releases
- 📦 Development artifacts
- 🔄 Continuous integration for development
- 🚧 Development deployment scripts

### 5. Version Bump (`.github/workflows/version-bump.yml`)

**Triggers**: Manual dispatch with version type selection

**Features**:
- 📈 Semantic version bumping (patch/minor/major)
- 🔀 Pre-release versioning (alpha/beta/rc)
- 📝 Automatic CHANGELOG.md updates
- 🔄 Pull request creation for review
- ✨ Automated commit messages
- 🏷️ Git tag creation

### 6. Deployment Status (`.github/workflows/deployment-status.yml`)

**Triggers**: Deployment events, workflow completions, releases

**Features**:
- 📊 Deployment status tracking
- 🎉 Success notifications with quick links
- ❌ Failure alerts with troubleshooting guides
- 📋 Detailed status reports
- 🔗 Status badge updates
- 📄 Automated artifact archiving

### 7. Test with Comments (`.github/workflows/test-with-comments.yml`)

**Triggers**: Pull requests to `main`, `develop`

**Features**:
- 🧪 Comprehensive testing with detailed reporting
- 💬 Rich PR comments with test results and coverage
- 📊 Visual progress bars for test metrics
- 📄 HTML and JSON test reports
- 🔍 Failed test details and debugging info
- 📈 Coverage visualization

## 🎯 Quick Start Guide

### Setting Up the Pipeline

1. **Enable GitHub Actions**:
   - Go to repository Settings → Actions → General
   - Allow "Read and write permissions" for GITHUB_TOKEN

2. **Configure GitHub Pages** (for documentation):
   - Go to Settings → Pages
   - Source: "GitHub Actions"

3. **Repository Secrets** (Optional):
   - All workflows use the default `GITHUB_TOKEN`
   - No additional secrets required for basic setup

### Creating Your First Release

1. **Version Bump**:
   ```bash
   # Option 1: Use GitHub UI
   Go to Actions → Version Bump → Run workflow
   Select version type (patch/minor/major)
   ```

   ```bash
   # Option 2: Manual tag
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **Review and Merge**:
   - Version bump creates a PR automatically
   - Review changes in CHANGELOG.md
   - Merge the PR

3. **Create Release**:
   - Go to Actions → Release → Run workflow
   - Or push a tag to trigger automatically

## 📊 Status Badges

Add these badges to your README.md:

```markdown
[![CI/CD Pipeline](https://github.com/SecCodeSmith/SecCodeSmith-backend/actions/workflows/ci.yml/badge.svg)](https://github.com/SecCodeSmith/SecCodeSmith-backend/actions/workflows/ci.yml)
[![Release](https://github.com/SecCodeSmith/SecCodeSmith-backend/actions/workflows/release.yml/badge.svg)](https://github.com/SecCodeSmith/SecCodeSmith-backend/actions/workflows/release.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Django 5.2+](https://img.shields.io/badge/django-5.2+-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

## 🔧 Workflow Details

### Test Pipeline Features
- **Parallel Testing**: Tests run on Python 3.10, 3.11, and 3.12
- **Service Integration**: PostgreSQL 15 and Redis 7 containers
- **Coverage Reports**: Automatically generated and commented on PRs
- **Quality Assurance**: flake8, black, isort, bandit, safety
- **Cache Optimization**: pip dependencies cached for faster builds

### Release Features
- **Semantic Versioning**: Automatic version detection from tags
- **Changelog Generation**: Git commits automatically formatted
- **Multi-format Artifacts**: tar.gz, zip, and Docker images
- **Documentation**: Automatic GitHub Pages deployment
- **Release Notes**: Formatted release descriptions

### Security Features
- **Minimal Permissions**: Each job has specific permission scopes
- **Token Security**: Uses GitHub's built-in GITHUB_TOKEN
- **Dependency Security**: Safety and bandit security scanning
- **Vulnerability Alerts**: Automated security issue detection

## 🛠️ Customization

### Modifying Test Configuration

Edit `.github/workflows/ci.yml`:

```yaml
# Add more Python versions
strategy:
  matrix:
    python-version: [3.10.x, 3.11.x, 3.12.x, 3.13.x]

# Add more test commands
- name: Run integration tests
  run: pytest tests/integration/
```

### Customizing Release Process

Edit `.github/workflows/release.yml`:

```yaml
# Change deployment target
- name: Deploy to production
  run: |
    # Your custom deployment script
    ./deploy-production.sh
```

### Adding Environment Variables

```yaml
env:
  DJANGO_SETTINGS_MODULE: SecCodeSmithBackend.production_settings
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

## 🚨 Troubleshooting

### Common Issues

1. **Tests Failing**:
   - Check test logs in Actions tab
   - Verify all dependencies are installed
   - Ensure test files are properly configured

2. **Deployment Failures**:
   - Verify GitHub Pages is enabled
   - Check repository permissions
   - Ensure build artifacts are generated

3. **Version Bump Issues**:
   - Verify VERSION file exists or will be created
   - Check Git permissions
   - Ensure CHANGELOG.md format is correct

### Debug Mode

Add this to any workflow for verbose logging:

```yaml
env:
  ACTIONS_STEP_DEBUG: true
```

## 📈 Monitoring and Analytics

### GitHub Insights
- View workflow runs in Actions tab
- Monitor deployment frequency
- Track test success rates
- Analyze build times

### Performance Optimization
- Use dependency caching
- Parallel job execution
- Minimal artifact sizes
- Efficient service containers

## 🤝 Contributing

When contributing to this repository:

1. Create feature branches: `feature/your-feature-name`
2. All PRs trigger automated testing
3. Ensure tests pass before requesting review
4. Follow semantic commit messages for changelog generation

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Django Testing Guide](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

💡 **Tip**: This pipeline is designed to be zero-configuration. Just push your code and let GitHub Actions handle the rest!

## 🔗 Quick Links

- [Main Repository](https://github.com/SecCodeSmith/SecCodeSmith-backend)
- [Actions Overview](https://github.com/SecCodeSmith/SecCodeSmith-backend/actions)
- [Latest Release](https://github.com/SecCodeSmith/SecCodeSmith-backend/releases/latest)
- [Issues](https://github.com/SecCodeSmith/SecCodeSmith-backend/issues)
- [Contributing Guide](https://github.com/SecCodeSmith/SecCodeSmith-backend/blob/main/CONTRIBUTING.md)
