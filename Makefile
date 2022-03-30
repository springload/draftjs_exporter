.PHONY: build clean-pyc init help test-ci
.DEFAULT_GOAL := help

help: ## See what commands are available.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36mmake %-15s\033[0m # %s\n", $$1, $$2}'

init: clean-pyc ## Install dependencies and initialise for development.
	pip install --upgrade pip setuptools wheel twine
	pip install -e .
	pip install -r requirements.txt
	nvm use
	npm install

lint: ## Lint the project.
	black --check **/*.py
	flake8 **/*.py
	isort --check-only --diff **/*.py
	mypy **/*.py

format: ## Format project files.
	isort **/*.py
	black **/*.py
	npm run format

test: ## Test the project.
	python -X dev -W error -m unittest discover

test-watch: ## Restarts the tests whenever a file changes.
	PYTHONDEVMODE=1 nodemon -q -e py -w tests -w draftjs_exporter  -x "clear && make test -s || true"

test-coverage: ## Run the tests while generating test coverage data.
	PYTHONDEVMODE=1 coverage run -m unittest discover && coverage report

test-ci: ## Continuous integration test suite.
	tox

dev: ## Restarts the example whenever a file changes.
	nodemon -q -e py -w tests -w draftjs_exporter -w example.py  -x "clear && python -X dev -W error example.py || true"

benchmark: ## Runs a one-off performance (speed, memory) benchmark.
	python benchmark.py

clean-pyc: ## Remove Python file artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

build: ## Builds package for publication.
	rm -f dist/*
	python -X dev -W error -m build

publish: build ## Publishes a new version to PyPI.
	twine upload dist/*
