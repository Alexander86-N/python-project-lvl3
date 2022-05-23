install:
	poetry install

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=page-loader --cov-report xml

lint:
	poetry run flake8 page-loader

gendiff:
	poetry run page-loader

build:
	poetry build

package-install:
	python3 -m pip install --force-reinstall --user dist/*.whl
