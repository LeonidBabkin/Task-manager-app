install:
		poetry install
build:
		poetry build
reinstall:
		pip install --user --force-reinstall dist/*.whl
dev:migrate
		poetry run python3 manage.py runserver
lint:
		poetry run flake8 task_manager
migrate:
		poetry run python3 manage.py makemigrations
		poetry run python3 manage.py migrate
shell:
		poetry run python3 manage.py shell
shellplus:
		poetry run python3 manage.py shell_plus --ipython
validatetemplates:
		poetry run python3 manage.py validate_templates
showurls:
		poetry run python3 manage.py show_urls
		PORT ?= 8000
start:
		poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi
lint:
	poetry run flake8

test:
	poetry run python3 manage.py test
cov:
	poetry run pytest --cov=task_manager
coverage:
	poetry run coverage run manage.py test task_manager
cc-cover:
	poetry run coverage xml
report-coverage:
	poetry run coverage report

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage report -m --include=task_manager/* --omit=task_manager/settings.py
	poetry run coverage xml --include=task_manager/* --omit=task_manager/settings.py

.PHONY: start, lint, migrate, shell, shellplus, validatetemplates, showurls, dev, reinstall, lint, test, testcov, cc-cover, report-coverage
