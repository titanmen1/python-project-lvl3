# Makefile
install:
	poetry install

run:
	poetry run page-loader

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python -m pip install dist/*.whl

pr:
	python -m pip uninstall hexlet-code -y

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest -vv

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml