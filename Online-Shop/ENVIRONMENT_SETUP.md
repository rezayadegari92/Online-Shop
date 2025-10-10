# Environment Variables Setup Guide

## 📋 Overview

This document explains how to configure environment variables for the Online Shop project.

## 🚀 Quick Setup

### Option 1: Using Setup Scripts

#### On Linux/Mac:
```bash
chmod +x setup_env.sh
./setup_env.sh
```

#### On Windows:
```cmd
setup_env.bat
```

### Option 2: Manual Setup

1. Copy the template:
   ```bash
   cp ENV_TEMPLATE.txt .env
   ```

2. Edit `.env` file and update the values as needed

## 📝 Environment Variables Reference

### Django Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | (provided) | Django secret key - **CHANGE IN PRODUCTION** |
| `DEBUG` | `True` | Enable debug mode (set to `False` in production) |
| `ALLOWED_HOSTS` | `*` | Comma-separated list of allowed hosts |

### Database Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_DB` | `onlineshop` | PostgreSQL database name |
| `POSTGRES_USER` | `onlineshop` | PostgreSQL username |
| `POSTGRES_PASSWORD` | `onlineshop` | PostgreSQL password |
| `POSTGRES_HOST` | `db` | PostgreSQL host (use `localhost` for local dev) |
| `POSTGRES_PORT` | `5432` | PostgreSQL port |

### Redis & Celery Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `CELERY_BROKER_URL` | `redis://redis:6379/0` | Celery broker URL |
| `CELERY_RESULT_BACKEND` | (same as broker) | Celery result backend URL |

### Email Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` | Email backend |
| `EMAIL_HOST` | `smtp.gmail.com` | SMTP server host |
| `EMAIL_PORT` | `587` | SMTP server port |
| `EMAIL_USE_TLS` | `True` | Use TLS for email |
| `EMAIL_HOST_USER` | (your email) | SMTP username/email |
| `EMAIL_HOST_PASSWORD` | (your password) | SMTP password |
| `DEFAULT_FROM_EMAIL` | (same as user) | Default sender email |

### JWT Token Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `JWT_ACCESS_TOKEN_LIFETIME_MINUTES` | `45` | Access token lifetime in minutes |
| `JWT_REFRESH_TOKEN_LIFETIME_DAYS` | `1` | Refresh token lifetime in days |
| `JWT_ROTATE_REFRESH_TOKENS` | `True` | Rotate refresh tokens on use |
| `JWT_BLACKLIST_AFTER_ROTATION` | `True` | Blacklist old tokens after rotation |

### API Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `API_PAGE_SIZE` | `10` | Default page size for API pagination |

## 🔒 Security Best Practices

### 1. Generate a Strong SECRET_KEY

For production, generate a new secret key:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 2. Gmail App Password Setup

If using Gmail for email:

1. Enable 2-Factor Authentication on your Google account
2. Visit https://myaccount.google.com/apppasswords
3. Generate an App Password
4. Use the App Password (not your regular password) in `EMAIL_HOST_PASSWORD`

### 3. Production Checklist

When deploying to production:

- [ ] Set `DEBUG=False`
- [ ] Change `SECRET_KEY` to a unique, strong value
- [ ] Update `ALLOWED_HOSTS` with your domain(s)
- [ ] Use strong database passwords
- [ ] Enable HTTPS and update security settings
- [ ] Review and update all default credentials
- [ ] Set up proper email configuration
- [ ] Configure backups for database and media files

## 🐳 Docker Environment Variables

The `.env` file is automatically loaded by Docker Compose. Variables are accessible in:

- Django application (via `os.getenv()`)
- Docker containers (defined in `docker-compose.yml`)

## 🔍 Troubleshooting

### Environment Variables Not Loading

1. Ensure `.env` file is in the `Online-Shop` directory
2. Check file permissions (should be readable)
3. Restart Docker containers: `docker-compose restart`
4. Check for syntax errors in `.env` file (no spaces around `=`)

### Email Not Sending

1. Verify Gmail App Password is correct
2. Check 2-Factor Authentication is enabled
3. Try with different email provider
4. Check SMTP settings match your provider

### Database Connection Issues

1. Verify database credentials in `.env`
2. Ensure PostgreSQL container is running: `docker-compose ps`
3. Check database logs: `docker-compose logs db`
4. Try connecting manually: `docker-compose exec db psql -U onlineshop`

## 📚 Additional Resources

- [Django Settings Documentation](https://docs.djangoproject.com/en/4.2/topics/settings/)
- [Docker Compose Environment Variables](https://docs.docker.com/compose/environment-variables/)
- [Gmail SMTP Settings](https://support.google.com/mail/answer/7126229)
- [PostgreSQL Environment Variables](https://www.postgresql.org/docs/current/libpq-envars.html)

## ⚠️ Important Notes

1. **Never commit `.env` to version control** - It contains sensitive information
2. The `.env` file should be in `.gitignore` (already configured)
3. Each team member should have their own `.env` file
4. Use different `.env` files for different environments (dev, staging, production)
5. Keep `ENV_TEMPLATE.txt` updated when adding new variables

## 🆘 Need Help?

If you encounter issues:

1. Check this documentation
2. Review the logs: `docker-compose logs`
3. Verify all required services are running: `docker-compose ps`
4. Ensure all environment variables are properly set
5. Contact the development team

---

**Last Updated:** 2025-01-10
**Version:** 1.0.0

