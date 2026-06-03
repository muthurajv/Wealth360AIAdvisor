import functools
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer("wealth360.agents")


def traced_agent(agent_name: str):
    """Wrap an agent node function with an OpenTelemetry span carrying business attributes."""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(state: dict, *args, **kwargs):
            with tracer.start_as_current_span(
                f"agent.{agent_name}",
                attributes={
                    "agent.name": agent_name,
                    "client.id": state.get("client_id", "unknown"),
                    "session.id": state.get("session_id", "unknown"),
                    "request.type": state.get("request_type", "unknown"),
                    "message.count": len(state.get("messages", [])),
                },
            ) as span:
                try:
                    result = fn(state, *args, **kwargs)
                    span.set_status(Status(StatusCode.OK))
                    return result
                except Exception as exc:
                    span.record_exception(exc)
                    span.set_status(Status(StatusCode.ERROR, str(exc)))
                    raise
        return wrapper
    return decorator
