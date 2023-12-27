include .env


pre-commit:
	pip install pre-commit --upgrade
	pre-commit install

up:
	docker compose -f docker-compose.yaml up --build -d

up-prod:
	docker compose -f docker-compose.prod.yaml up -d

up-dev:
	docker compose -f docker-compose.dev.yaml up -d

logs:
	docker compose logs -f --no-log-prefix backend
	
logs-db:
	docker compose logs -f db

logs-celery:
	docker compose logs -f --no-log-prefix worker

logs-scanner:
	docker compose logs -f --no-log-prefix scanner_eth

down:
	docker compose down

shell:
	docker compose exec backend python -m ptpython

shell-sql:
	docker compose exec db psql postgresql://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@$(POSTGRES_SERVER):$(POSTGRES_PORT)/$(POSTGRES_DB)

shell-redis:
	docker compose exec redis redis-cli

revision:
	docker compose exec backend alembic revision --autogenerate

upgrade:
	docker compose exec backend alembic upgrade head

downgrade:
	docker compose exec backend alembic downgrade head


clean-migrations:
	find . -path "*/alembic/versions/*.py" -not -path "*/venv/*" -not -path "*/__init__.py" -delete

clean-db:
	rm -rf .docker

clean-redis:
	rm -rf .docker/redis-data

clean: clean-db clean-migrations


init-db:
	docker compose exec backend python src/db/init_db.py

