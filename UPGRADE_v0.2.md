# Upgrade notes from HelaCare v0.1

This archive is source-complete but intentionally does not ship a real `.env` file or `node_modules`.

## Start from this archive
```powershell
Copy-Item .env.example .env
docker compose up --build
```

The API automatically runs Alembic migrations, including `0002_platform_features`.

If you already have the original 20 plants in your Docker volume, log in to `/admin/login` and click **Rebuild index** once so those legacy rows get pgvector embeddings.

If the DB is empty, import the spreadsheet:
```powershell
docker compose exec api python -m app.scripts.import_plants /data/raw/HelaCare_Traditional_Plants_V1.xlsx
```

Default local admin credentials are shown in `.env.example`. Change the password and JWT secret before using the project outside local development.
