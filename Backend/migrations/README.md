# Database Migrations

This directory contains database migration files created by Flask-Migrate.

## Initializing Migrations

If this is the first time setting up the project:

```bash
flask db init
```

This will create the migrations directory structure.

## Creating Migrations

After making changes to models:

```bash
flask db migrate -m "Description of changes"
```

## Applying Migrations

To apply migrations to the database:

```bash
flask db upgrade
```

## Rolling Back Migrations

To rollback the last migration:

```bash
flask db downgrade
```

## Migration Best Practices

1. Always review generated migration files before applying
2. Test migrations on a development database first
3. Backup production database before applying migrations
4. Use descriptive migration messages
5. Keep migrations small and focused

