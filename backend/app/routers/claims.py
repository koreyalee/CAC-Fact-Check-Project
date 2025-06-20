from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Claim(BaseModel):
    id: int
    text: str
    verified: bool
    evidence: List[str]

claims_db = []

@router.post("/claims/", response_model=Claim)
def ingest_claim(claim: Claim):
    claims_db.append(claim)
    return claim

@router.get("/claims/", response_model=List[Claim])
def get_claims():
    return claims_db

@router.get("/claims/{claim_id}", response_model=Claim)
def get_claim(claim_id: int):
    for claim in claims_db:
        if claim.id == claim_id:
            return claim
    raise HTTPException(status_code=404, detail="Claim not found")