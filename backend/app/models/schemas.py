from pydantic import BaseModel
from typing import List, Optional

class Claim(BaseModel):
    id: str
    text: str
    veracity: str
    evidence: List[str]

class FactCheckRequest(BaseModel):
    claims: List[Claim]

class FactCheckResponse(BaseModel):
    claims: List[Claim]

class SummaryRequest(BaseModel):
    claims: List[Claim]

class SummaryResponse(BaseModel):
    summary: str
    claims: List[Claim]

class NarrativeTracking(BaseModel):
    narrative_id: str
    claims: List[Claim]
    platforms: List[str]