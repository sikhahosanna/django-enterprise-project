15/9/26

# Docker Setup

## 1. Installation

Install Docker Desktop and make sure Docker is running.

Verify Docker installation:

```powershell
docker --version
docker compose version
```

Navigate to the project directory:

```powershell
cd C:\Users\BlackRoth\Desktop\django\myproject
```

## 2. Environment Variables

Create a `.env` file in the project root directory.

Required environment variables:

```env
SECRET_KEY=your-secret-key
DB_NAME=mydb
DB_USER=postgres
DB_PASSWORD=your-database-password
DB_HOST=postgres
DB_PORT=5432

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
REDIS_CACHE_URL=redis://redis:6379/1
```

Do not commit real passwords, secret keys, or other sensitive information to Git.

## 3. Build Commands

Build the Docker images:

```powershell
docker compose build
```

Rebuild without cache:

```powershell
docker compose build --no-cache
```

## 4. Start Commands

Start the complete application:

```powershell
docker compose up -d
```

Check running containers:

```powershell
docker compose ps
```

The application contains:

* Django Web
* PostgreSQL
* Redis
* Celery
* Nginx

## 5. Stop Commands

Stop the running containers:

```powershell
docker compose stop
```

Stop and remove containers and network:

```powershell
docker compose down
```

The PostgreSQL named volume is preserved when using `docker compose down`.

## 6. Logs

View logs for all services:

```powershell
docker compose logs
```

Django logs:

```powershell
docker compose logs web
```

Celery logs:

```powershell
docker compose logs celery
```

PostgreSQL logs:

```powershell
docker compose logs postgres
```

Redis logs:

```powershell
docker compose logs redis
```

Nginx logs:

```powershell
docker compose logs nginx
```

Follow logs continuously:

```powershell
docker compose logs -f
```

## 7. Troubleshooting

### Port 8000 Already in Use

Check the running containers:

```powershell
docker compose ps
```

Stop the container using the port if required:

```powershell
docker stop <container_name>
```

Then start the application:

```powershell
docker compose up -d
```

### Containers Are Not Running

Check all containers:

```powershell
docker compose ps -a
```

Check the logs of a service:

```powershell
docker compose logs <service_name>
```

### Database Connection Problem

Check PostgreSQL:

```powershell
docker compose ps postgres
```

The Docker database host should be:

```text
postgres
```

Run migrations:

```powershell
docker compose exec web python manage.py migrate
```

Check Django:

```powershell
docker compose exec web python manage.py check
```

### Redis Connection Problem

Check Redis:

```powershell
docker compose exec redis redis-cli ping
```

Expected result:

```text
PONG
```

### Celery Problem

Check Celery logs:

```powershell
docker compose logs celery
```

Test Celery:

```powershell
docker compose exec celery celery -A myproject inspect ping
```

Expected result:

```text
pong
```

### Nginx Problem

Check Nginx logs:

```powershell
docker compose logs nginx
```

Test the API through Nginx:

```powershell
curl http://localhost/api/docs/
```

A `200 OK` response confirms that Nginx can communicate with Django.

## Application URLs

Django API:

```text
http://localhost/api/v1/
```

Swagger API Documentation:

```text
http://localhost/api/docs/
```

OpenAPI Schema:

```text
http://localhost/api/schema/
```

## Docker Services

| Service  | Purpose                                |
| -------- | -------------------------------------- |
| web      | Django application running with Daphne |
| postgres | PostgreSQL database                    |
| redis    | Redis cache and message broker         |
| celery   | Background task processing             |
| nginx    | Reverse proxy                          |

## Verification

Start the complete application:

```powershell
docker compose up -d
```

Check all services:

```powershell
docker compose ps
```

All services should show `Up`.

Verify the API through Nginx:

```powershell
curl http://localhost/api/docs/
```

A successful `200 OK` response confirms that the Docker environment and Nginx-to-Django communication are working correctly.
