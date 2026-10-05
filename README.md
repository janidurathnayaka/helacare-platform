# HelaCare v0.2 — Curated Knowledge + DevOps Platform

HelaCare is a source-grounded Sri Lankan traditional-health knowledge assistant and curator platform. It is designed for educational information retrieval, not diagnosis, dosage, or prescribing.

## Included in v0.2

### Public assistant
- Next.js chat UI with English/Sinhala mode
- deterministic emergency red-flag safety gate
- verified-record-only answer composition
- source links and chat audit trail
- user helpful/not-helpful feedback

### Admin / Curator Console
Open `http://localhost:3000/admin/login`.
- JWT-protected admin login
- Dashboard and work queue
- Plants: add, edit, verify, delete
- Sources: add and review evidence records
- Practitioner Reviews
- User Feedback queue
- Safety Flags generated from urgent chats
- Analytics for language, triage and recent queries
- Admin Audit Log

### Grounded RAG / pgvector
- PostgreSQL 18 + pgvector
- multilingual alias lookup
- lexical retrieval
- deterministic 256-dimension vector fallback over verified records
- curator-triggered reindexing
- source-grounded templated answers (no free-form medical generation)

### DevOps
- Docker Compose local stack
- GitHub Actions CI
- GitHub Container Registry CD workflow
- Trivy container security scan in CI
- Prometheus metrics endpoint and server
- Grafana with Prometheus datasource provisioning
- production Docker Compose + Nginx reverse proxy example
- deployment, admin and RAG documentation

## Quick start

1. Copy environment template:

```powershell
Copy-Item .env.example .env
```

2. Edit `.env` and at minimum change:
- `ADMIN_PASSWORD`
- `JWT_SECRET`

3. Start everything:

```powershell
docker compose up --build
```

4. URLs:
- Web: http://localhost:3000
- Admin: http://localhost:3000/admin/login
- API docs: http://localhost:8000/docs
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001

5. Import the dataset if your DB is empty:

```powershell
docker compose exec api python -m app.scripts.import_plants /data/raw/HelaCare_Traditional_Plants_V1.xlsx
```

6. Log into Admin and click **Rebuild index** once after importing legacy rows.

Default development admin from `.env.example`:
- email: `admin@helacare.local`
- password: `change-me-now`

Change these before deployment.

## Safety
HelaCare preserves a strict separation between documented traditional use and clinically established treatment. The system does not provide dosage advice and urgent symptom patterns bypass herbal retrieval in favor of an emergency-care warning.

See `docs/SAFETY.md`, `docs/ADMIN.md`, `docs/RAG.md`, and `docs/DEPLOYMENT.md`.

## GitHub-ready workflow

This package intentionally excludes `.env`, `node_modules`, `.next`, caches, and Git history.

After extracting the project:

```powershell
Copy-Item .env.example .env
docker compose up --build
```

For a new GitHub repository:

```powershell
git init
git add .
git commit -m "Initial HelaCare release"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/helacare-platform.git
git push -u origin main
```

CI runs automatically on pushes to `main` and `develop`. Container vulnerability scans are informational so newly disclosed base-image CVEs do not turn the whole learning-project pipeline red. The container delivery workflow is manual and can be run after repository settings are configured.
