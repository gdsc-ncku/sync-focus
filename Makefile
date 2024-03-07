migrate:
	poetry run alembic -c alembic.ini upgrade head

revision:
ifndef MESSAGE
	$(error MESSAGE is not set)
endif
	poetry run alembic -c alembic.ini revision --autogenerate -m "${MESSAGE}"

setup-database:
	sudo docker compose up db
