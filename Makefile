migrate:
	poetry run alembic -c alembic.ini upgrade head

revision:
ifndef MESSAGE
	$(error MESSAGE is not set)
endif
	poetry run alembic -c alembic.ini revision --autogenerate -m "${MESSAGE}"

run:
	OTEL_TRACES_EXPORTER=otlp_proto_http OTEL_EXPORTER_OTLP_ENDPOINT=127.0.0.1:4318 OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true uvicorn app:app --reload

dev:
	uvicorn app:app --reload

setup-database:
	sudo docker compose --profile backend-dev up

clear-revision:
	rm -rf alembic/versions/*

clear-db: clear-revision
	rm -rf .volume/*
