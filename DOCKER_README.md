# Docker Setup for Little Lemon Restaurant

This project includes Docker Compose configuration to run both the Django backend and React frontend in containers.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. **Build and start all services:**
   ```bash
   docker-compose up --build
   ```

2. **Access the applications:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

3. **Stop the services:**
   ```bash
   docker-compose down
   ```

## Development Mode

For development with live reloading:

```bash
# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Rebuild specific service
docker-compose build backend
docker-compose build frontend
```

## Database Setup

The Django backend will use SQLite by default. If you need to run migrations:

```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py populate_db
```

## Troubleshooting

- If port conflicts occur, modify the ports in `docker-compose.yml`
- For fresh start: `docker-compose down -v && docker-compose up --build`
- Check logs: `docker-compose logs [service-name]`