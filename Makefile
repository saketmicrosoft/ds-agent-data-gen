.PHONY: setup lint type test security run

setup:
	python -m pip install --upgrade pip
	python -m pip install -e .[dev]

lint:
	ruff check .
	ruff format --check .

type:
	mypy src

test:
	pytest

security:
	bandit -q -r src
	pip-audit

run:
	autodata run-inner-loop --budget 3
