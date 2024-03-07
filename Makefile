migrate:
	poetry run alembic -c alembic.ini upgrade head

revision:
ifndef MESSAGE
	$(error MESSAGE is not set)
endif
	poetry run alembic -c alembic.ini revision --autogenerate -m "${MESSAGE}"

run:
	poetry run uvicorn app:app --reload