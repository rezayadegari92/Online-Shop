# Database Migration Guide for Dokploy

This guide helps you migrate your database from local Docker to Dokploy container.

## Prerequisites

1. Access to your Dokploy database credentials
2. PostgreSQL client tools installed (or use Docker)
3. Network access to Dokploy database

## Method 1: Using Python Script (Recommended)

### Step 1: Export Current Database

```bash
# From your local machine or inside Docker container
python migrate_to_dokploy.py --export
```

This will create a SQL backup file like `backup_20251221_142048.sql`

### Step 2: Import to Dokploy

Set your Dokploy database credentials:

```bash
export DOKPLOY_DB_HOST=your-dokploy-db-host
export DOKPLOY_DB_PORT=5432
export DOKPLOY_DB_NAME=onlineshop
export DOKPLOY_DB_USER=onlineshop
export DOKPLOY_DB_PASSWORD=your-password
```

Then import:

```bash
python migrate_to_dokploy.py --import backup_20251221_142048.sql
```

### Step 3: Or Do Full Migration in One Step

```bash
export DOKPLOY_DB_HOST=your-dokploy-db-host
export DOKPLOY_DB_PASSWORD=your-password
python migrate_to_dokploy.py --migrate
```

## Method 2: Using Shell Script

### Export

```bash
chmod +x migrate_to_dokploy.sh
./migrate_to_dokploy.sh export
```

### Import

```bash
export DOKPLOY_DB_HOST=your-dokploy-db-host
export DOKPLOY_DB_PASSWORD=your-password
./migrate_to_dokploy.sh import backup_20251221_142048.sql
```

### Full Migration

```bash
export DOKPLOY_DB_HOST=your-dokploy-db-host
export DOKPLOY_DB_PASSWORD=your-password
./migrate_to_dokploy.sh migrate
```

## Method 3: Manual Migration

### Step 1: Export from Docker

```bash
docker compose exec db pg_dump -U onlineshop -d onlineshop \
  --clean --if-exists --no-owner --no-acl > backup.sql
```

### Step 2: Import to Dokploy

```bash
export PGPASSWORD=your-dokploy-password
psql -h your-dokploy-host -p 5432 -U onlineshop -d onlineshop -f backup.sql
unset PGPASSWORD
```

## Getting Dokploy Database Credentials

1. Log into your Dokploy dashboard
2. Navigate to your application/database
3. Find the database connection details:
   - Host
   - Port (usually 5432)
   - Database name
   - Username
   - Password

## Troubleshooting

### Connection Issues

If you can't connect to Dokploy database:

1. **Check network access**: Make sure you can reach the Dokploy host
2. **Check firewall**: Ensure port 5432 is open
3. **Check credentials**: Verify username and password
4. **Use Dokploy's internal network**: If running from Dokploy container, use internal hostname

### Permission Issues

If you get permission errors:

- Make sure the database user has CREATE, DROP, and INSERT permissions
- Some Dokploy setups require specific user permissions

### Large Database

For large databases:

1. Use compression:
   ```bash
   pg_dump ... | gzip > backup.sql.gz
   gunzip -c backup.sql.gz | psql ...
   ```

2. Use custom format (faster):
   ```bash
   pg_dump -Fc ... > backup.dump
   pg_restore -d dokploy_db backup.dump
   ```

## After Migration

1. **Verify data**: Check that all tables and data are present
2. **Update Django settings**: Update `DATABASES` in `settings.py` to point to Dokploy
3. **Run migrations**: Run `python manage.py migrate` to ensure schema is up to date
4. **Test application**: Verify all functionality works with new database

## Rollback

If something goes wrong, you can restore from backup:

```bash
# Export from Dokploy
pg_dump -h dokploy-host -U user -d db > dokploy_backup.sql

# Import back to local
psql -h localhost -U onlineshop -d onlineshop -f dokploy_backup.sql
```

