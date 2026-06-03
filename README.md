# Wealth360 AI Advisor Copilot — POC

A 3-agent LangGraph system for wealth management advisors. Built with Azure OpenAI, Pinecone, FastAPI, and OpenTelemetry → Grafana Cloud.

## Architecture

```
User → FastAPI → LangGraph Supervisor
                      ├── Advisor Agent    (portfolio, meeting prep, recommendations)
                      ├── Research Agent   (market trends, PDFs, analyst opinions)
                      └── Compliance Agent (policy checks, suitability, restricted list)
```

## Quickstart

```bash
# 1. Copy env file and edit with your credentials
copy .env.example .env

# 2. Run the API (stub data works out of the box — no Azure/Pinecone needed)
uvicorn wealth360.api.app:app --reload

# 3. Open interactive docs
start http://localhost:8000/docs
```

## Environment Variables

| Variable | Description | Required for real run |
|---|---|---|
| `USE_STUB_DATA` | `true` = use in-memory stubs (default) | — |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI key | Yes |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | Yes |
| `AZURE_OPENAI_DEPLOYMENT` | Chat model deployment name (e.g. `gpt-4o`) | Yes |
| `PINECONE_API_KEY` | Pinecone API key | Yes |
| `PINECONE_INDEX_NAME` | Pinecone index name | Yes |
| `OTEL_ENABLED` | Enable OTLP trace export | Optional |
| `GRAFANA_OTLP_ENDPOINT` | Grafana Cloud OTLP endpoint | If OTEL_ENABLED=true |
| `GRAFANA_OTLP_TOKEN` | Base64 `instanceId:apiToken` | If OTEL_ENABLED=true |
| `GRAFANA_CLOUD_URL` | Grafana stack URL | For dashboard deploy |
| `GRAFANA_API_TOKEN` | Grafana service account token (Editor) | For dashboard deploy |

## Grafana Cloud Setup

1. Add OTEL + dashboard credentials to `.env`
2. Set `OTEL_ENABLED=true`
3. Deploy the dashboard:

```bash
python -m wealth360.observability.grafana.deploy_dashboard
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/advisor/copilot` | Supervisor-routed copilot (main entry point) |
| `POST` | `/api/v1/advisor/meeting-prep` | Pre-meeting briefing |
| `GET` | `/api/v1/advisor/portfolio/{client_id}` | Portfolio summary |
| `GET` | `/api/v1/advisor/risk/{client_id}` | Risk overview |
| `POST` | `/api/v1/research/analyze` | Research query |
| `POST` | `/api/v1/research/summarize-pdf` | Summarize a PDF |
| `GET` | `/api/v1/research/analyst/{ticker}` | Analyst opinions |
| `GET` | `/api/v1/research/trends/{sector}` | Market trends |
| `POST` | `/api/v1/compliance/validate` | Policy compliance check |
| `POST` | `/api/v1/compliance/suitability` | Product suitability |
| `POST` | `/api/v1/compliance/restricted-screen` | Restricted securities screen |

## Running Tests

```bash
python -m pytest tests/ -v
```

## Switching from Stubs to Real Azure + Pinecone

Set in `.env`:

```ini
USE_STUB_DATA=false
AZURE_OPENAI_API_KEY=<your-key>
AZURE_OPENAI_ENDPOINT=<your-endpoint>
PINECONE_API_KEY=<your-key>
```

No code changes needed — the graph topology and all agents are unchanged.
