import opentelemetry.trace
import opentelemetry.trace.status
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)

tracer_provider = TracerProvider(
    resource=Resource.create({SERVICE_NAME: "sync-focus_backend"})
)
tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
tracer = opentelemetry.trace.get_tracer(
    instrumenting_module_name="edu.ncku.gdsc.gcp.sync-focus.backend",
    tracer_provider=tracer_provider,
)


def trace(span_name, **attrs):
    def decorator(f):
        def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(span_name) as decorated_span:
                for key, value in attrs.items():
                    decorated_span.set_attribute(key, str(value))
                try:
                    return f(*args, **kwargs)
                except Exception as err:
                    decorated_span.set_status(
                        opentelemetry.trace.status.Status(
                            opentelemetry.trace.status.StatusCode.ERROR, str(err)
                        )
                    )
                    raise err

        return wrapper

    return decorator
