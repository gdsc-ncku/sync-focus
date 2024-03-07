import opentelemetry

tracer = opentelemetry.trace.get_tracer("edu.ncku.gdsc.gcp.sync-focus.backend")

def trace(span_name, **attrs):
    def decorator(f):
        def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(span_name) as decorated_span:
                for key, value in attrs.items():
                    decorated_span.set_attribute(key, str(value))
                try:                      
                    return f(*args, **kwargs)
                except Exception as err:
                    decorated_span.set_status(opentelemetry.trace.status.Status(opentelemetry.trace.status.StatusCode.ERROR, str(err)))
                    raise err
        return wrapper
    return decorator
