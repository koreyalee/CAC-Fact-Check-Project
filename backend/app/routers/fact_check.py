from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from ..services.rag import perform_fact_check
from ..models.schemas import Claim, FactCheckResult

router = APIRouter()

class FactCheckRequest(BaseModel):
    claims: List[Claim]

class FactCheckResponse(BaseModel):
    results: List[FactCheckResult]

@router.post("/fact-check", response_model=FactCheckResponse)
async def fact_check(request: FactCheckRequest):
    try:
        results = perform_fact_check(request.claims)
        return FactCheckResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))