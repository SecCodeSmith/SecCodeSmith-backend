# Docker Deployment Guide

## 🐳 Container Registry Setup

This project automatically builds and pushes Docker containers to container registries when a release is created.

### Supported Registries

1. **GitHub Container Registry (ghcr.io)** - Automatic, no setup required
2. **Docker Hub** - Requires setup (optional)

### GitHub Container Registry

The Docker image is automatically published to:
```
ghcr.io/seccodesmith/seccodesmith-backend:latest
ghcr.io/seccodesmith/seccodesmith-backend:v0.2.0
```

### Docker Hub Setup (Optional)

To enable Docker Hub publishing, add these secrets to your GitHub repository:

1. Go to your repository → Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username
   - `DOCKERHUB_TOKEN`: Your Docker Hub access token

**Creating a Docker Hub Access Token:**
1. Log in to Docker Hub
2. Go to Account Settings → Security → Access Tokens
3. Create a new access token with Read, Write, Delete permissions

## 🚀 Using the Container

### Pull and Run

```bash
# From GitHub Container Registry
docker pull ghcr.io/seccodesmith/seccodesmith-backend:latest
docker run -p 8000:8000 ghcr.io/seccodesmith/seccodesmith-backend:latest

# From Docker Hub (if configured)
docker pull seccodesmith/seccodesmith-backend:latest
docker run -p 8000:8000 seccodesmith/seccodesmith-backend:latest
```

### With Environment Variables

```bash
docker run -p 8000:8000 \
  -e DJANGO_DEBUG=False \
  -e SECRET_KEY=your-secret-key \
  -e DATABASE_URL=postgres://user:pass@host:5432/db \
  ghcr.io/seccodesmith/seccodesmith-backend:latest
```

### Using Docker Compose

```yaml
version: '3.8'
services:
  backend:
    image: ghcr.io/seccodesmith/seccodesmith-backend:latest
    ports:
      - "8000:8000"
    environment:
      - DJANGO_DEBUG=False
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: backend
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

## 🔧 Development

### Building Locally

```bash
# Build the image
docker build -t seccodesmith-backend .

# Run locally
docker run -p 8000:8000 seccodesmith-backend
```

### Multi-architecture Build

The release workflow builds for both AMD64 and ARM64 architectures:

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t seccodesmith-backend .
```

## 📋 Container Features

- **Base Image**: Alpine Linux 3.22 (lightweight and secure)
- **Python**: 3.x with virtual environment
- **Web Server**: Gunicorn with optimized configuration
- **Database Support**: PostgreSQL client included
- **Security**: Non-root user, minimal attack surface
- **Caching**: Docker layer caching enabled in CI/CD

## 🛡️ Security

- Container runs as non-root user
- Minimal base image (Alpine Linux)
- Security scanning included in CI/CD pipeline
- Regular base image updates
- Secrets managed through environment variables

## 📦 Release Process

1. Create a new tag: `git tag -a v1.0.0 -m "Release v1.0.0"`
2. Push the tag: `git push origin v1.0.0`
3. GitHub Actions automatically:
   - Builds multi-architecture containers
   - Pushes to configured registries
   - Updates the release with container information

## 🔍 Monitoring

Container health can be monitored through:
- Django health check endpoint: `/admin/`
- Container logs: `docker logs <container_id>`
- Resource usage: `docker stats <container_id>`
