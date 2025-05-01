from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, SessionLocal


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Travel Itinerary Manager")

from fastapi.openapi.utils import get_openapi

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/itineraries/", response_model=schemas.ItineraryOut, summary="Create a new trip itinerary", response_description="The created itinerary")
def create_itinerary(itinerary: schemas.ItineraryCreate, db: Session = Depends(get_db)):
    """
    Create a new trip itinerary with day-wise hotel accommodations, transfers, and activities.
    """
    db_itinerary = models.Itinerary(name=itinerary.name, nights=itinerary.nights)
    db.add(db_itinerary)
    db.commit()
    db.refresh(db_itinerary)

    for day_data in itinerary.days:
        db_day = models.Day(
            day_number=day_data.day_number,
            hotel=day_data.hotel,
            transfer=day_data.transfer,
            itinerary_id=db_itinerary.id
        )
        db.add(db_day)
        db.commit()
        db.refresh(db_day)

        for activity in day_data.activities:
            db.add(models.Activity(name=activity.name, location=activity.location, day_id=db_day.id))
    
    db.commit()
    return db_itinerary

@app.get("/itineraries/", response_model=List[schemas.ItineraryOut], summary="View existing trip itineraries", response_description="List of itineraries")
def get_itineraries(db: Session = Depends(get_db)):
    """
    Retrieve all existing trip itineraries with their details.
    """
    return db.query(models.Itinerary).all()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Travel Itinerary Manager API",
        version="1.0.0",
        description="API for managing trip itineraries with day-wise accommodations, transfers, and activities.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
