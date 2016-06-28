
init:
	pip install -r requirements.txt

lint:
	flake8 draft_exporter
	isort --check-only --diff --recursive draft_exporter

test:
	python -m unittest discover

test_watch:
	nodemon -q -e py -w tests -w draft_exporter  -x "make test || true"
