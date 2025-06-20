from fastapi import APIRouter, HTTPException
from typing import List
from ..services.rag import generate_summary
from ..models.schemas import SummaryRequest, SummaryResponse

router = APIRouter()

@router.post("/summaries", response_model=SummaryResponse)
async def create_summary(summary_request: SummaryRequest):
    try:
        summary = await generate_summary(summary_request.claims)
        return SummaryResponse(summary=summary)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))