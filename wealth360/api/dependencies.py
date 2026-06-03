from fastapi import Request
from wealth360.config.settings import Settings, get_settings


def get_graph(request: Request):
    return request.app.state.graph


def get_app_settings() -> Settings:
    return get_settings()
