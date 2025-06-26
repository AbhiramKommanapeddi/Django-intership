# Redis Installation Guide for Windows

## Method 1: Using Docker (Recommended)

### Install Docker Desktop

1. Download Docker Desktop from: https://www.docker.com/products/docker-desktop/
2. Install and start Docker Desktop
3. Run Redis container:

```bash
# Run Redis in Docker
docker run -d -p 6379:6379 --name redis-server redis:alpine

# Check if Redis is running
docker ps

# Test Redis connection
docker exec -it redis-server redis-cli ping
```

## Method 2: Using WSL2 (Ubuntu)

### Install Redis in WSL

```bash
# Enter WSL
wsl

# Update package list
sudo apt update

# Install Redis
sudo apt install redis-server

# Start Redis
sudo service redis-server start

# Test Redis
redis-cli ping
```

## Method 3: Native Windows Installation

### Download Redis for Windows

1. Go to: https://github.com/microsoftarchive/redis/releases
2. Download the latest `.msi` file
3. Install and start the Redis service

## Method 4: Using Windows Package Manager

```powershell
# Install using winget (Windows 10+)
winget install Redis.Redis
```

## Verify Installation

After installing Redis using any method, test the connection:

```bash
# Test Redis connection
redis-cli ping
# Should return: PONG

# Check Redis info
redis-cli info server
```

## Configure for Django

1. Make sure Redis is running on `localhost:6379`
2. Your Django settings already include:
   ```python
   CELERY_BROKER_URL = 'redis://localhost:6379/0'
   CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
   ```

## Start Redis Server

### Docker:

```bash
docker start redis-server
```

### WSL:

```bash
wsl sudo service redis-server start
```

### Windows Service:

Redis should start automatically as a Windows service.

## Troubleshooting

### Connection Refused Error

- Make sure Redis server is running
- Check if port 6379 is available
- Verify firewall settings

### Permission Errors (WSL)

```bash
sudo chown redis:redis /var/lib/redis
sudo service redis-server restart
```

Once Redis is running, you can proceed with testing Celery integration!
