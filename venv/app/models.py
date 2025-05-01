from sqlalchemy import Column, Integer, String, ForeignKey, Date, Index
from sqlalchemy.orm import relationship
from app.database import Base

class Itinerary(Base):
    __tablename__ = "itineraries"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True, nullable=False)
    nights = Column(Integer, nullable=False)
    days = relationship("Day", back_populates="itinerary", cascade="all, delete-orphan")

    __table_args__ = (
        Index('ix_itinerary_name_nights', 'name', 'nights'),
    )

class Day(Base):
    __tablename__ = "days"
    id = Column(Integer, primary_key=True)
    day_number = Column(Integer, nullable=False)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id", ondelete="CASCADE"), nullable=False)
    hotel = Column(String, nullable=False)
    transfer = Column(String, nullable=True)
    activities = relationship("Activity", back_populates="day", cascade="all, delete-orphan")
    itinerary = relationship("Itinerary", back_populates="days")

    __table_args__ = (
        Index('ix_day_itinerary_day_number', 'itinerary_id', 'day_number', unique=True),
    )

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    day_id = Column(Integer, ForeignKey("days.id", ondelete="CASCADE"), nullable=False)
    day = relationship("Day", back_populates="activities")
