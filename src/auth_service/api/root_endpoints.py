from fastapi import APIRouter
from starlette.responses import RedirectResponse

from configs.config import app_settings
from constants.backend import BACKEND_ENTRYPOINT
from schemas.service import ServiceInfo

router = APIRouter()


@router.get(f"/{BACKEND_ENTRYPOINT}/sentry-debug/")
async def trigger_error() -> None:
    1 / 0  # noqa: B018


@router.get(f"/{BACKEND_ENTRYPOINT}/", response_model=ServiceInfo)
async def root() -> ServiceInfo:
    return ServiceInfo(
        name_service=app_settings.SERVICE_NAME,
        version=app_settings.SERVICE_VERSION,
    )


@router.get("/")
async def home() -> RedirectResponse:
    return RedirectResponse(f"/{BACKEND_ENTRYPOINT}")
