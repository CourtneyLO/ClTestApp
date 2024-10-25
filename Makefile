FILE_PATH=$(shell pwd)
SPLIT_PATH=$(subst /, ,$(FILE_PATH))
USERS_NAME=$(word 2,$(SPLIT_PATH))

# Virtual Environment

venv:
	python3 -m venv virtualenvironment

requirements:
	pip freeze > requirements.txt

install:
	pip install --trusted-host=pypi.org --trusted-host=files.pythonhosted.org -r requirements.txt

uninstall:
	pip uninstall -r requirements.txt -y

remove-venv:
	rm -r virtualenvironment/


# Database
install-postgresql:
	brew install postgresql

start-db:
	brew services start postgresql

restart-db:
	brew services restart postgresql

stop-db:
	brew services stop postgresql

db-user:
	createuser -Ps deploymen_test_app_cl_root_user

db:
	createdb -O deploymen_test_app_cl_root_user deploymen_test_app_cl_db

access-db:
	psql -d deploymen_test_app_cl_db -U deploymen_test_app_cl_root_user -Ws

migration:
	python3 manage.py makemigrations

migrate:
	python3 manage.py migrate

create-all-tables:
	python3 manage.py makemigrations;
	python3 manage.py migrate

drop-all-tables:
	python3 scripts/drop-all-tables.py

create-su:
	python3 manage.py createsuperuser

populate:
	./manage.py loaddata populate-database.json


# App

app:
	python3 manage.py startapp ${name}

run:
	python3 manage.py runserver

static:
	python3 manage.py collectstatic
# Zappa
# These commands will only work if you have your usename as a stage with the correct settings in the zappa_settings.json

update-my-dev:
	zappa update '${USERS_NAME}'

deploy-logs:
	zappa tail '${USERS_NAME}'

zappa-migrate:
	zappa update '${USERS_NAME}';
	zappa manage '${USERS_NAME}' migrate

create-db:
	zappa manage '${USERS_NAME}' create_pg_db

create-user:
	zappa manage '${USERS_NAME}' create_admin_user


# Tests

tests:
	./manage.py test --pattern="*_tests.py"

test:
	./manage.py test --pattern="*_tests.py" ${app}



## Infrastructure

install-prerequisites:
	brew install terraform@1.0

init:
	cd infrastructure; terraform init

fmt:
	cd infrastructure; terraform fmt

validate:
	cd infrastructure; terraform validate

plan:
	cd infrastructure; TF_VAR_ENVIRONMENT='${USERS_NAME}' terraform plan

apply:
	cd infrastructure; TF_VAR_ENVIRONMENT='${USERS_NAME}' terraform apply

destroy:
	cd infrastructure; TF_VAR_ENVIRONMENT='${USERS_NAME}' terraform destroy


# Linter
lint:
	pylint --load-plugins pylint_django --django-settings-module=main.settings **/*.py
