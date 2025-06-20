from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, index=True)
    verified = Column(String, index=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_claim(db: SessionLocal, content: str):
    db_claim = Claim(content=content, verified="pending")
    db.add(db_claim)
    db.commit()
    db.refresh(db_claim)
    return db_claim

def get_claim(db: SessionLocal, claim_id: int):
    return db.query(Claim).filter(Claim.id == claim_id).first()

def update_claim_verification(db: SessionLocal, claim_id: int, verified: str):
    claim = get_claim(db, claim_id)
    if claim:
        claim.verified = verified
        db.commit()
        db.refresh(claim)
    return claim

def get_all_claims(db: SessionLocal):
    return db.query(Claim).all()