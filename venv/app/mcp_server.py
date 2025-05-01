from typing import List
from fastapi import FastAPI
from sqlalchemy.orm import Session, joinedload
from app.database import SessionLocal
from app.models import Itinerary, Day
from app.schemas import ItineraryOut

mcp_app = FastAPI(title="MCP Server")

@mcp_app.get("/recommendation/{nights}", response_model=List[ItineraryOut])
def recommend(nights: int):
    db: Session = SessionLocal()
    results = db.query(Itinerary).options(joinedload(Itinerary.days).joinedload(Day.activities)).filter(Itinerary.nights == nights).all()
    db.close()
    return results
