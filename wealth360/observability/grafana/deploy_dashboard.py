"""
Deploy the Wealth360 dashboard to Grafana Cloud.

Usage:
    python -m wealth360.observability.grafana.deploy_dashboard

Requires in .env:
    GRAFANA_CLOUD_URL=https://your-stack.grafana.net
    GRAFANA_API_TOKEN=your-service-account-token-with-editor-role
"""
import json
import sys
from pathlib import Path
import requests
from wealth360.config.settings import get_settings


def deploy() -> None:
    s = get_settings()

    if s.grafana_api_token == "stub-grafana-api-token":
        print("ERROR: Set GRAFANA_API_TOKEN and GRAFANA_CLOUD_URL in .env before deploying.")
        sys.exit(1)

    dashboard_path = Path(__file__).parent / "dashboard.json"
    dashboard = json.loads(dashboard_path.read_text())

    payload = {
        "dashboard": dashboard,
        "folderId": 0,
        "overwrite": True,
        "message": "Deployed by wealth360 deploy_dashboard.py",
    }

    url = f"{s.grafana_cloud_url.rstrip('/')}/api/dashboards/db"
    headers = {
        "Authorization": f"Bearer {s.grafana_api_token}",
        "Content-Type": "application/json",
    }

    print(f"Deploying dashboard to {url} ...")
    resp = requests.post(url, json=payload, headers=headers, timeout=30)

    if resp.status_code in (200, 201):
        data = resp.json()
        dashboard_url = f"{s.grafana_cloud_url.rstrip('/')}{data.get('url', '')}"
        print(f"Dashboard deployed successfully.")
        print(f"URL: {dashboard_url}")
    else:
        print(f"ERROR {resp.status_code}: {resp.text}")
        sys.exit(1)


if __name__ == "__main__":
    deploy()
