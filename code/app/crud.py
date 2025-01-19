from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext
from typing import List, Optional
from sqlalchemy import func

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_park(db: Session, park_id: int) -> Optional[models.Park]:
    return db.query(models.Park).filter(models.Park.id == park_id).first()


def get_parks(db: Session, skip: int = 0, limit: int = 100) -> List[models.Park]:
    return db.query(models.Park).offset(skip).limit(limit).all()


def create_park(db: Session, park: schemas.ParkCreate):
    # Create the park in the database
    db_park = models.Park(
        name=park.name,
        description=park.description,
        images=park.images,
        latitude=park.location.latitude,  # Assuming location is a nested object with latitude
        longitude=park.location.longitude  # and longitude
    )
    
    # Add and commit the new park to the database
    db.add(db_park)
    db.commit()
    db.refresh(db_park)
    
    # Return the park as a Pydantic model, not the raw SQLAlchemy model
    return schemas.Park(
        id=db_park.id,
        name=db_park.name,
        description=db_park.description,
        location=schemas.Location(latitude=db_park.latitude, longitude=db_park.longitude),
        images=db_park.images,
        created_at=db_park.created_at,
        updated_at=db_park.updated_at
    )



def update_park(db: Session, park_id: int, park: schemas.ParkCreate) -> Optional[models.Park]:
    db_park = get_park(db, park_id)
    if db_park:
        db_park.name = park.name
        if park.location:  # Check if location is provided
            db_park.latitude = park.location.latitude
            db_park.longitude = park.location.longitude
        db_park.description = park.description
        db_park.images = park.images
        db.commit()
        db.refresh(db_park)

        # Manually return the location details within the park
        db_park.location = schemas.Location(
            latitude=db_park.latitude,
            longitude=db_park.longitude
        )

        return db_park
    return None


def delete_park(db: Session, park_id: int) -> bool:
    db_park = get_park(db, park_id)
    if db_park:
        db.delete(db_park)
        db.commit()
        return True
    return False


def get_species(db: Session, skip: int = 0, limit: int = 100) -> List[models.Species]:
    return db.query(models.Species).offset(skip).limit(limit).all()


def get_species_by_id(db: Session, species_id: int) -> Optional[models.Species]:
    return db.query(models.Species).filter(models.Species.id == species_id).first()


def get_species_by_park(db: Session, park_id: int) -> List[models.Species]:
    return db.query(models.Species).filter(models.Species.park_id == park_id).all()


def create_species(db: Session, species: schemas.SpeciesCreate) -> models.Species:
    db_species = models.Species(
        name=species.name,
        scientific_name=species.scientific_name,
        park_id=species.park_id,
        description=species.description,
        image=species.image,
    )
    db.add(db_species)
    db.commit()
    db.refresh(db_species)
    return db_species


def update_species(db: Session, species_id: int, species: schemas.SpeciesCreate) -> Optional[models.Species]:
    db_species = get_species_by_id(db, species_id)
    if db_species:
        db_species.name = species.name
        db_species.scientific_name = species.scientific_name
        db_species.park_id = species.park_id
        db_species.description = species.description
        db_species.image = species.image
        db.commit()
        db.refresh(db_species)
        return db_species
    return None


def delete_species(db: Session, species_id: int) -> bool:
    db_species = get_species_by_id(db, species_id)
    if db_species:
        db.delete(db_species)
        db.commit()
        return True
    return False


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    print(f"Trying to create user {user.username}")
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    print(f"user {db_user.username} created with id {db_user.id}")
    return db_user

def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user_role(db: Session, user_id: int, role:str) -> Optional[models.User]:
  db_user = get_user_by_id(db, user_id)
  if db_user:
    db_user.role = role
    db.commit()
    db.refresh(db_user)
    return db_user
  return None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    print(f"plain_password = {plain_password}, hashed_password = {hashed_password}")
    return pwd_context.verify(plain_password, hashed_password)


def get_rows_count(db:Session, model):
  return db.query(func.count(model.id)).scalar()