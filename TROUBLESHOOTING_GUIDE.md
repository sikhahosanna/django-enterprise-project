# Production Troubleshooting Guide

## Purpose

This guide helps identify common production issues by checking the correct service, logs, and commands.

## 1. Django / Application Not Working

**Problem:** API is not responding or returns application errors.

**Where to check:** Django/Gunicorn logs.

**Command:**

```bash
docker compose logs web --tail 50
```

**Possible solution:**

* Check Django errors and tracebacks.
* Verify the web container is running.
* Check environment variables.
* Restart the web service if required:

```bash
docker compose restart web
```

---

## 2. Nginx / HTTPS Issue

**Problem:** API is not accessible through HTTP/HTTPS.

**Where to check:** Nginx logs.

**Command:**

```bash
docker compose logs nginx --tail 50
```

**Possible solution:**

* Check Nginx configuration.
* Verify ports `80` and `443`.
* Verify SSL certificate and key files.
* Restart Nginx:

```bash
docker compose restart nginx
```

---

## 3. Gunicorn Issue

**Problem:** Django application is not starting behind Gunicorn.

**Where to check:** Web container logs.

**Command:**

```bash
docker compose logs web --tail 50
```

**Possible solution:**

* Check Gunicorn startup errors.
* Verify `myproject.asgi:application`.
* Verify Gunicorn and Uvicorn Worker installation.
* Rebuild the web image:

```bash
docker compose up -d --build web
```

---

## 4. Celery Task Not Executing

**Problem:** Background task remains pending or does not execute.

**Where to check:** Celery logs.

**Command:**

```bash
docker compose logs celery --tail 50
```

**Possible solution:**

* Check whether the Celery worker is running.
* Verify Redis broker configuration.
* Verify the required Celery queue is being consumed.
* Check registered tasks.
* Restart Celery:

```bash
docker compose restart celery
```

---

## 5. PostgreSQL Database Issue

**Problem:** Database connection fails or queries produce errors.

**Where to check:** PostgreSQL logs.

**Command:**

```bash
docker compose logs postgres --tail 50
```

**Possible solution:**

* Check whether PostgreSQL is accepting connections.
* Verify database environment variables.
* Check Django database configuration.
* Run Django system checks:

```bash
docker compose exec web python manage.py check
```

* Run migrations:

```bash
docker compose exec web python manage.py migrate
```

---

## 6. Redis Issue

**Problem:** Redis-dependent features are not working.

**Where to check:** Redis container and application/Celery logs.

**Commands:**

```bash
docker compose logs redis --tail 50
```

```bash
docker compose exec redis redis-cli ping
```

**Expected result:**

```text
PONG
```

**Possible solution:**

* Verify the Redis container is running.
* Check Redis connection configuration.
* Restart Redis if required:

```bash
docker compose restart redis
```

---

## 7. Health Check Failure

**Problem:** Production health endpoint reports `unhealthy`.

**Where to check:** Health endpoint and related service logs.

**Commands:**

```bash
curl.exe -k https://localhost/api/health/
```

```bash
curl.exe -k https://localhost/api/health/database/
```

```bash
curl.exe -k https://localhost/api/health/redis/
```

**Possible solution:**

* If database health fails, check PostgreSQL logs.
* If Redis health fails, check Redis configuration and Redis logs.
* If the main health check fails, check Django/Gunicorn logs.

---

## 8. Quick Service Status

**Problem:** Need to know whether all production services are running.

**Where to check:** Docker Compose service status.

**Command:**

```bash
docker compose ps
```

**Possible solution:**
Identify the stopped service and inspect its logs:

```bash
docker compose logs <service-name> --tail 50
```

Then restart or rebuild the affected service if required.

---

## Troubleshooting Flow

```text
Problem
   ↓
Identify affected service
   ↓
Check service status
   ↓
Inspect service logs
   ↓
Identify error
   ↓
Check configuration / connectivity
   ↓
Apply solution
   ↓
Restart or rebuild service if required
   ↓
Run health checks
   ↓
Verify API again
```

## Useful Commands

### Check all containers

```bash
docker compose ps
```

### View logs

```bash
docker compose logs <service-name> --tail 50
```

### Restart a service

```bash
docker compose restart <service-name>
```

### Rebuild and start a service

```bash
docker compose up -d --build <service-name>
```

### Check Django

```bash
docker compose exec web python manage.py check
```

### Check migrations

```bash
docker compose exec web python manage.py migrate
```

### Check Redis

```bash
docker compose exec redis redis-cli ping
```

## Production Safety

* Do not expose passwords, secret keys, database credentials, JWT secrets, or Redis credentials in logs.
* Do not share `.env` files publicly.
* Check logs before restarting services to identify the actual problem.
* After fixing an issue, verify the relevant health endpoint and API.
