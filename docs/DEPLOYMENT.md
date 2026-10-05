# HelaCare deployment

## Local development
1. Copy `.env.example` to `.env` and change `ADMIN_PASSWORD` + `JWT_SECRET`.
2. `docker compose up --build`
3. Web: http://localhost:3000
4. API docs: http://localhost:8000/docs
5. Admin: http://localhost:3000/admin/login
6. Prometheus: http://localhost:9090
7. Grafana: http://localhost:3001

After migration, import the workbook if the database is empty:
`docker compose exec api python -m app.scripts.import_plants /data/raw/HelaCare_Traditional_Plants_V1.xlsx`
Then log in as admin and use **Rebuild index** once to populate all pgvector embeddings.

## Production
Use `deploy/docker-compose.prod.yml` on a Linux VM or container host. Create `.env.production` outside version control and provide strong secrets. Set `API_IMAGE` and `WEB_IMAGE` to images published by `.github/workflows/cd.yml`.

Terminate TLS with your cloud load balancer or replace the Nginx service with a TLS-enabled reverse proxy. Do not expose PostgreSQL, Redis, Prometheus or Grafana publicly without authentication/network controls.
