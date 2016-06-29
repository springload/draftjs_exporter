.PHONY: help
.DEFAULT_GOAL := help

help: ## See what commands are available.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36mmake %-15s\033[0m # %s\n", $$1, $$2}'

init: ## Install dependencies and initialise for development.
	pip install -r requirements.txt

lint: ## Lint the project.
	flake8 draft_exporter --max-line-length 120
	isort --check-only --diff --recursive draft_exporter
	flake8 tests --max-line-length 1200
	isort --check-only --diff --recursive tests

test: ## Test the project.
	python -m unittest discover

test_watch: ## Restarts the tests whenever a file changes.
	nodemon -q -e py -w tests -w draft_exporter  -x "clear && make test -s || true"

test_ci: lint test ## Check for continuous integration.

dev: ## Restarts the example whenever a file changes.
	nodemon -q -e py -w tests -w draft_exporter  -x "clear && python example.py || true"
