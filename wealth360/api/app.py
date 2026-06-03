from contextlib import asynccontextmanager
from fastapi import FastAPI
from wealth360.observability.setup import setup_telemetry
from wealth360.agents.supervisor import build_graph
from wealth360.api.routers import advisor, research, compliance


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_telemetry()
    app.state.graph = build_graph()
    yield
    from opentelemetry import trace
    trace.get_tracer_provider().force_flush()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Wealth360 AI Advisor Copilot",
        version="0.1.0",
        description="3-agent LangGraph system for wealth management advisors",
        lifespan=lifespan,
    )

    try:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        FastAPIInstrumentor.instrument_app(app)
    except ImportError:
        pass

    app.include_router(advisor.router, prefix="/api/v1/advisor", tags=["Advisor"])
    app.include_router(research.router, prefix="/api/v1/research", tags=["Research"])
    app.include_router(compliance.router, prefix="/api/v1/compliance", tags=["Compliance"])

    @app.get("/health", tags=["System"])
    def health():
        return {"status": "ok", "service": "wealth360-advisor"}

    return app


app = create_app()
