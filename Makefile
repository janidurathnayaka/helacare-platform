.PHONY: up down logs build test api-test web-lint import-data rag-reindex prod-config

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

build:
	docker compose build

test: api-test web-lint

api-test:
	docker compose run --rm api pytest -q

web-lint:
	docker compose run --rm web npm run lint

import-data:
	docker compose exec api python -m app.scripts.import_plants /data/raw/HelaCare_Traditional_Plants_V1.xlsx

prod-config:
	docker compose -f deploy/docker-compose.prod.yml config
