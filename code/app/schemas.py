from pydantic import BaseModel
from typing import Optional, List

class Location(BaseModel):
    latitude: float
    longitude: float


class ParkBase(BaseModel):
    name: str
    description: str
    location: Location
    images: Optional[str] = None
    
class ParkCreate(ParkBase):
  pass


class Park(ParkBase):
    id: int
    created_at : Optional[str] = None
    updated_at : Optional[str] = None
    class Config:
        orm_mode = True


class SpeciesBase(BaseModel):
    name: str
    scientific_name: Optional[str] = None
    park_id: int
    description: Optional[str] = None
    image: Optional[str] = None
class SpeciesCreate(SpeciesBase):
    pass

class Species(SpeciesBase):
    id: int
    created_at : Optional[str] = None
    updated_at : Optional[str] = None
    class Config:
        orm_mode = True

class UserBase(BaseModel):
  username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str
    created_at : Optional[str] = None
    updated_at : Optional[str] = None

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class WeatherData(BaseModel):
    temperature: float
    description: str
    humidity: int
    wind_speed: float