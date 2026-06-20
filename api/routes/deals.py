"""
Deal management routes.
"""

import uuid

from fastapi import APIRouter, HTTPException

from api.models.request_models import DealCreateRequest
from api.models.response_models import DealResponse
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()

# In-memory deal store (in production, use Postgres)
_deals: dict[str, dict] = {}


@router.post("/deals", response_model=DealResponse)
async def create_deal(request: DealCreateRequest):
    """Creates a new deal."""
    deal_id = str(uuid.uuid4())
    _deals[deal_id] = {
        "deal_id": deal_id,
        "deal_name": request.deal_name,
        "description": request.description,
        "document_count": 0,
        "status": "active",
    }

    logger.info(
        "Deal created",
        extra={"deal_id": deal_id, "deal_name": request.deal_name},
    )

    return DealResponse(**_deals[deal_id])


@router.get("/deals", response_model=list[DealResponse])
async def list_deals():
    """Lists all deals."""
    return [DealResponse(**d) for d in _deals.values()]


@router.get("/deals/{deal_id}", response_model=DealResponse)
async def get_deal(deal_id: str):
    """Gets a specific deal by ID."""
    if deal_id not in _deals:
        raise HTTPException(status_code=404, detail=f"Deal not found: {deal_id}")
    return DealResponse(**_deals[deal_id])
