migrate:
	poetry run alembic -c alembic.ini upgrade head

revision:
ifndef MESSAGE
	$(error MESSAGE is not set)
endif
	poetry run alembic -c alembic.ini revision --autogenerate -m "${MESSAGE}"

run:
	OTEL_EXPORTER_OTLP_ENDPOINT=127.0.0.1:4317 OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true opentelemetry-instrument --traces_exporter otlp_proto_grpc --metrics_exporter otlp_proto_grpc --logs_exporter console,otlp_proto_grpc --service_name edu.ncku.gdsc.gcp.sync-focus.backend uvicorn app:app --reload

setup-database:
	sudo docker compose up db
