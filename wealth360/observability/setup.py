import base64
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from wealth360.config.settings import get_settings


def setup_telemetry() -> TracerProvider:
    s = get_settings()

    resource = Resource.create({
        SERVICE_NAME: s.otel_service_name,
        SERVICE_VERSION: "0.1.0",
        "deployment.environment": s.app_env,
    })

    provider = TracerProvider(resource=resource)

    if s.otel_enabled and s.grafana_otlp_token != "stub-token":
        headers = {"Authorization": f"Basic {s.grafana_otlp_token}"}
        otlp_exporter = OTLPSpanExporter(
            endpoint=f"{s.grafana_otlp_endpoint}/v1/traces",
            headers=headers,
        )
        provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    else:
        # Console exporter for local dev — prints spans to stdout
        provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

    trace.set_tracer_provider(provider)
    return provider
