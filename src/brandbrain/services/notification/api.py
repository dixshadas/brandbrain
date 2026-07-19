from __future__ import annotations

from fastapi import APIRouter, Depends

from brandbrain.platform.auth import Principal, get_principal

from .interface import NotificationEngine
from .schemas import Notification, PulseDigest
from .service import NotificationEngineImpl

router = APIRouter(prefix="/v1/notifications", tags=["Notification Engine"])


def get_service() -> NotificationEngine:
    return NotificationEngineImpl()


@router.get("", response_model=list[Notification], summary="In-app notification inbox")
async def inbox(brand_id: str, principal: Principal = Depends(get_principal),
                svc: NotificationEngine = Depends(get_service)) -> list[Notification]:
    return await svc.list_inbox(brand_id, principal)


@router.post("/{notification_id}/read", response_model=Notification, summary="Mark read")
async def mark_read(notification_id: str, principal: Principal = Depends(get_principal),
                    svc: NotificationEngine = Depends(get_service)) -> Notification:
    return await svc.mark_read(notification_id, principal)


@router.get("/pulse", response_model=PulseDigest, summary="Weekly Brand Pulse digest")
async def pulse(brand_id: str, principal: Principal = Depends(get_principal),
                svc: NotificationEngine = Depends(get_service)) -> PulseDigest:
    return await svc.build_pulse(brand_id, principal)
