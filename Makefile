.PHONY: venv install test smoke fmt lint compose-up compose-down

venv:
	python -m venv .venv && . .venv/Scripts/activate && pip install -e .

install:
	pip install -e . && pip install pytest

test:
	pytest -q

smoke:
	maher --text samples.txt || true
	@echo "Wrote output/analysis.txt (if model reachable)."

fmt:
	python -m pip install ruff && ruff format .

lint:
	python -m pip install ruff && ruff check .

compose-up:
	docker compose -f deploy/docker/docker-compose.lab.yml up -d --build

compose-down:
	docker compose -f deploy/docker/docker-compose.lab.yml down
