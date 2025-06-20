from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import claims, fact_check, summaries

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(claims.router, prefix="/claims", tags=["claims"])
app.include_router(fact_check.router, prefix="/fact-check", tags=["fact-check"])
app.include_router(summaries.router, prefix="/summaries", tags=["summaries"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Fact Checker API!"}