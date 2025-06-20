from typing import List, Dict, Any
from fastapi import HTTPException
import requests

class RAGService:
    def __init__(self, model_endpoint: str):
        self.model_endpoint = model_endpoint

    def ingest_content(self, content: str) -> str:
        # Ingest content into the RAG model
        response = requests.post(f"{self.model_endpoint}/ingest", json={"content": content})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to ingest content")
        return response.json().get("message", "Content ingested successfully")

    def identify_claims(self, content: str) -> List[Dict[str, Any]]:
        # Identify claims in the provided content
        response = requests.post(f"{self.model_endpoint}/identify_claims", json={"content": content})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to identify claims")
        return response.json().get("claims", [])

    def fact_check_claim(self, claim: str) -> Dict[str, Any]:
        # Fact-check a specific claim
        response = requests.post(f"{self.model_endpoint}/fact_check", json={"claim": claim})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fact-check claim")
        return response.json()

    def generate_summary(self, claims: List[str]) -> str:
        # Generate a summary based on the claims
        response = requests.post(f"{self.model_endpoint}/generate_summary", json={"claims": claims})
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to generate summary")
        return response.json().get("summary", "")