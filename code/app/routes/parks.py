from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.db import get_db
from app.auth import get_current_user, get_admin_user
import requests
from typing import Optional


router = APIRouter(prefix="/parks", tags=["parks"])


@router.get("/", response_model=List[schemas.Park])
def read_parks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    parks = crud.get_parks(db, skip=skip, limit=limit)
    return [
        schemas.Park(
            id=park.id,
            name=park.name,
            description=park.description,
            location=schemas.Location(latitude=park.latitude, longitude=park.longitude),
            images=park.images,
            created_at=park.created_at,
            updated_at=park.updated_at
        )
        for park in parks
    ]


@router.get("/{park_id}", response_model=schemas.Park)
def read_park(park_id: int, db: Session = Depends(get_db)):
    db_park = crud.get_park(db, park_id=park_id)
    if db_park is None:
        raise HTTPException(status_code=404, detail="Park not found")
    
    # Map the db_park (SQLAlchemy model) to the Pydantic schema
    return schemas.Park(
        id=db_park.id,
        name=db_park.name,
        description=db_park.description,
        location=schemas.Location(latitude=db_park.latitude, longitude=db_park.longitude),
        images=db_park.images,
        created_at=db_park.created_at,
        updated_at=db_park.updated_at
    )


@router.post("/", response_model=schemas.Park, status_code=status.HTTP_201_CREATED)
def create_park(
    park: schemas.ParkCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user),
):
    return crud.create_park(db, park)


@router.put("/{park_id}", response_model=schemas.Park)
def update_park(
    park_id: int,
    park: schemas.ParkCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user),
):
    db_park = crud.update_park(db, park_id=park_id, park=park)
    if db_park is None:
        raise HTTPException(status_code=404, detail="Park not found")
    return db_park


@router.delete("/{park_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_park(
    park_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user),
):
    if not crud.delete_park(db, park_id=park_id):
        raise HTTPException(status_code=404, detail="Park not found")
    return None


@router.get("/{park_id}/weather", response_model=schemas.WeatherData)
async def get_weather(park_id: int, db: Session = Depends(get_db)):
    db_park = crud.get_park(db, park_id=park_id)
    if db_park is None:
        raise HTTPException(status_code=404, detail="Park not found")
    latitude = db_park.latitude
    longitude = db_park.longitude

    api_key = "1b1c332cdf1e8c7cae8983a059a8b56f"  
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    response = requests.get(weather_url)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    weather_data = response.json()
    if weather_data:
      return {
          "temperature": weather_data["main"]["temp"],
          "description": weather_data["weather"][0]["description"],
          "humidity": weather_data["main"]["humidity"],
          "wind_speed": weather_data["wind"]["speed"],
      }
    else:
        raise HTTPException(status_code=404, detail="Weather data not found")
    
