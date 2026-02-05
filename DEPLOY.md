# Deployment Guide

## Production Architecture
- **Web Server**: Nginx (Reverse Proxy, SSL termination, Static files)
- **App Server**: Gunicorn (WSGI Server)
- **Database**: PostgreSQL (Managed Service or Docker)
- **Process Manager**: Docker Compose or Systemd

## Steps

### 1. Environment Configuration
Ensure `.env` is secure on production.
- `DEBUG=False`
- `SECRET_KEY`: Use a strong, random string.
- `ALLOWED_HOSTS`: Set to your domain name (e.g., `crm.example.com`).

### 2. Static Files
Django doesn't serve static files efficiently in production.
1. Run `python manage.py collectstatic`.
2. Configure Nginx to serve the `staticfiles/` directory at `/static/`.

### 3. Gunicorn Setup
Run Gunicorn referencing the WSGI app:
```bash
gunicorn mini_crm.wsgi:application --bind 0.0.0.0:8000
```
Recommended to run via Docker or Systemd.

### 4. Nginx Configuration
Example snippet:
```nginx
server {
    listen 80;
    server_name crm.example.com;

    location /static/ {
        alias /path/to/app/staticfiles/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 5. Database Migrations and Backups
- **Migrations**: Always run `python manage.py migrate` after deployment.
- **Backups**: Use `pg_dump` to backup PostgreSQL database regularly.
  ```bash
  pg_dump -U postgres minicrm > backup.sql
  ```
