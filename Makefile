LOG_DIR:= .logs
DATA_DIR:= data
CERT_DIR:= /etc/letsencrypt/live/pylinks.hopto.org
.PHONY: init lint test coverage


init:
	git config core.hooksPath .hooks

lint:
	pipenv run black -l 120 pyli
	git ls-files -- . ':!:*__init__.py' -z | while IFS= read -rd '' f; do tail -c1 < "$f" | read -r _ || echo >> "$f"; done
	pipenv run isort -rc .

test:
	pipenv run python -m pytest --cov=pyli tests --cov-report xml

coverage:
	pipenv run python -m pytest --cov=pyli tests --cov-report term-missing