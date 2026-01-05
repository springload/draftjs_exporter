.PHONY: build clean-pyc init help test-compatibility
.DEFAULT_GOAL := help

help: ## See what commands are available.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "- `make %s`: %s\n", $$1, $$2}'

init: clean-pyc ## Install dependencies and initialize for development.
	uv venv
	uv sync --dev
	nvm use
	npm install

lint: ## Lint the project.
	ruff check
	ruff format --check
	mypy draftjs_exporter tests
	ty check

format: ## Format project files.
	ruff format
	npm run format

test: ## Test the project.
	PYTHONDEVMODE=1 pytest -W error --capture=no

test-watch: ## Restarts the tests whenever a file changes.
	PYTHONDEVMODE=1 nodemon -q -e py -w tests -w draftjs_exporter  -x "clear && make test -s || true"

test-coverage: ## Run the tests while generating test coverage data.
	PYTHONDEVMODE=1 pytest -W error --cov --cov-report=html --capture=no

test-compatibility: ## Compatibility-focused test suite.
	uv run --isolated --python 3.10 --with 'beautifulsoup4==4.7.1, html5lib==1.1, lxml==4.6.5' pytest

dev: ## Restarts the example whenever a file changes.
	nodemon -q -e py -w tests -w draftjs_exporter -w example.py  -x "clear && python -X dev -W error example.py || true"

benchmark: ## Runs a one-off performance (speed, memory) benchmark.
	python benchmark.py
	python -m memray summary benchmark.bin
	python -m memray stats benchmark.bin

clean-pyc: ## Remove Python file artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

build: ## Builds package for publication.
	rm -f dist/*
	uv build

publish: build ## Publishes a new version to PyPI.
	uv publish
