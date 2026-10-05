# Upload HelaCare to a new GitHub repository

This folder is prepared as a clean GitHub-ready project. It does not contain `.git`, `.env`, `node_modules`, or `.next`.

## 1. Create a new empty GitHub repository

Create a repository named `helacare-platform`.

Do **not** add a README, `.gitignore`, or license on GitHub because this project already contains its own files.

## 2. Open the extracted project in PowerShell

```powershell
cd "PATH\TO\helacare-platform"
```

## 3. Create your local environment file

```powershell
Copy-Item .env.example .env
```

Edit `.env` and change at least `ADMIN_PASSWORD` and `JWT_SECRET` before deployment.

## 4. Test locally with Docker

```powershell
docker compose up --build
```

Useful URLs:

- Web: http://localhost:3000
- Admin: http://localhost:3000/admin/login
- API docs: http://localhost:8000/docs
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001

## 5. Initialize Git and upload

Replace `YOUR-USERNAME` with your GitHub username.

```powershell
git init
git add .
git commit -m "Initial HelaCare GitHub-ready release"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/helacare-platform.git
git push -u origin main
```

## 6. GitHub Actions

The CI workflow runs automatically. It checks:

- API install, Ruff, and pytest
- Web TypeScript checks and Next.js build
- API and Web Docker image builds
- Trivy HIGH/CRITICAL vulnerability reports

Trivy is intentionally informational (`exit-code: 0`) so a newly disclosed vulnerability in a base image does not make the complete learning-project CI pipeline red.

The container delivery workflow is manual. Run it from **GitHub > Actions > HelaCare Container Delivery > Run workflow** when you are ready to publish images to GHCR.
