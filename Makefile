.PHONY: install dev backend frontend test lint fmt

install:
	pip install -e ".[dev,excel]"
	cd frontend && npm install

dev:
	$(MAKE) backend &
	$(MAKE) frontend &
	wait

backend:
	uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

frontend:
	cd frontend && npm start

test:
	pytest

lint:
	ruff check backend/
	mypy backend/ --ignore-missing-imports

fmt:
	ruff format backend/
	ruff check --fix backend/
