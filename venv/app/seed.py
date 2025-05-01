from app.database import SessionLocal
from app.models import Itinerary, Day, Activity

def seed_data():
    db = SessionLocal()

    # Clear existing data
    db.query(Activity).delete()
    db.query(Day).delete()
    db.query(Itinerary).delete()
    db.commit()

    # Sample data for Phuket and Krabi regions
    itineraries = [
        {
            "name": "Phuket Adventure",
            "nights": 3,
            "days": [
                {
                    "day_number": 1,
                    "hotel": "Patong Beach Hotel",
                    "transfer": "Airport to Hotel",
                    "activities": [
                        {"name": "Beach Relaxation", "location": "Patong Beach"},
                        {"name": "Night Market Visit", "location": "Patong"}
                    ]
                },
                {
                    "day_number": 2,
                    "hotel": "Patong Beach Hotel",
                    "transfer": "Hotel to Phi Phi Islands",
                    "activities": [
                        {"name": "Snorkeling", "location": "Phi Phi Islands"},
                        {"name": "Boat Tour", "location": "Phi Phi Islands"}
                    ]
                },
                {
                    "day_number": 3,
                    "hotel": "Patong Beach Hotel",
                    "transfer": "Hotel to Airport",
                    "activities": [
                        {"name": "Shopping", "location": "Jungceylon Mall"}
                    ]
                }
            ]
        },
        {
            "name": "Krabi Relaxation",
            "nights": 5,
            "days": [
                {
                    "day_number": 1,
                    "hotel": "Ao Nang Resort",
                    "transfer": "Airport to Resort",
                    "activities": [
                        {"name": "Beach Walk", "location": "Ao Nang Beach"}
                    ]
                },
                {
                    "day_number": 2,
                    "hotel": "Ao Nang Resort",
                    "transfer": "Resort to Railay Beach",
                    "activities": [
                        {"name": "Rock Climbing", "location": "Railay Beach"},
                        {"name": "Cave Exploration", "location": "Phra Nang Cave"}
                    ]
                },
                {
                    "day_number": 3,
                    "hotel": "Ao Nang Resort",
                    "transfer": "Resort to Island Tour",
                    "activities": [
                        {"name": "Island Hopping", "location": "Four Islands"},
                        {"name": "Kayaking", "location": "Ao Thalane"}
                    ]
                },
                {
                    "day_number": 4,
                    "hotel": "Ao Nang Resort",
                    "transfer": "Resort Leisure Day",
                    "activities": [
                        {"name": "Spa Day", "location": "Resort Spa"}
                    ]
                },
                {
                    "day_number": 5,
                    "hotel": "Ao Nang Resort",
                    "transfer": "Resort to Airport",
                    "activities": [
                        {"name": "Local Market Visit", "location": "Krabi Town"}
                    ]
                }
            ]
        }
    ]

    for itinerary_data in itineraries:
        itinerary = Itinerary(name=itinerary_data["name"], nights=itinerary_data["nights"])
        db.add(itinerary)
        db.commit()
        db.refresh(itinerary)

        for day_data in itinerary_data["days"]:
            day = Day(
                day_number=day_data["day_number"],
                hotel=day_data["hotel"],
                transfer=day_data["transfer"],
                itinerary_id=itinerary.id
            )
            db.add(day)
            db.commit()
            db.refresh(day)

            for activity_data in day_data["activities"]:
                activity = Activity(
                    name=activity_data["name"],
                    location=activity_data["location"],
                    day_id=day.id
                )
                db.add(activity)
        db.commit()

    db.close()

if __name__ == "__main__":
    seed_data()
