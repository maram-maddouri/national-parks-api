from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Park, Species, User # Import Park from models
from app import crud, schemas
from typing import List
from sqlalchemy import func


DATABASE_URL = "sqlite:///./tunisia_parks.db"

# Initialize the SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Initialize the database by creating all tables and seeding data.
    """
    print('Attempting to create tables')
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()


def get_db():
    """
    Dependency for getting a new database session.
    """
    print(f"trying to get db session")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def seed_data(db):
    """
    Seed the database with initial data if not already present.
    """
    # Check if data is already present
    print("Seed data method has started")
    print(f"current row count = {crud.get_rows_count(db, Park)}")
    if crud.get_rows_count(db, Park) > 0:
        print("Parks are found in the database, existing seed data method")
        return

    # Define initial parks data
    initial_parks = [
        schemas.ParkCreate(
            name="Ichkeul National Park",
            location=schemas.Location(latitude=37.15, longitude=9.666),
            description="A beautiful national park in northern Tunisia.",
            images="https://example.com/ichkeul1.jpg,https://example.com/ichkeul2.jpg"
        ),
        schemas.ParkCreate(
            name="Boukornine National Park",
            location=schemas.Location(latitude=36.742, longitude=10.266),
            description="A national park with unique mountains and flora",
            images="https://example.com/boukornine1.jpg,https://example.com/boukornine2.jpg"
        ),
    ]

    # Define initial species data
    initial_species = [
        schemas.SpeciesCreate(
            name="African Golden Wolf",
            scientific_name="Canis anthus",
            park_id=1,
            description="A medium-sized canid native to North Africa.",
            image="https://example.com/wolf.jpg"
        ),
        schemas.SpeciesCreate(
            name="Barbary Macaque",
            scientific_name="Macaca sylvanus",
            park_id=1,
            description="A species of macaque found in the Atlas Mountains.",
            image="https://example.com/macaque.jpg"
        ),
        schemas.SpeciesCreate(
            name="Atlas Cedar",
            scientific_name="Cedrus atlantica",
            park_id=2,
            description="A species of cedar native to the Atlas Mountains.",
            image="https://example.com/atlas-cedar.jpg"
        ),
    ]

    # Define initial users data
    initial_users = [
        schemas.UserCreate(
            username="john_doe_123",
            password="StrongP@$$wOrd123",
        ),
        schemas.UserCreate(
            username="jane.smith.456",
            password="AnotherS3cr3t!",
        ),
        schemas.UserCreate(
            username="admin_user_789",
            password="AdminPasswOrd1!",
        ),
    ]

    # Create parks
    for park_data in initial_parks:
        park = crud.create_park(db, park_data)
        print(f"park {park.name} created with id {park.id}")

    # Create species
    for species_data in initial_species:
        species = crud.create_species(db, species_data)
        print(f"species {species.name} created with id {species.id}")

    # Create users and set admin role if applicable
    for user_data in initial_users:
        user = crud.create_user(db, user_data)
        print(f"user {user.username} created with id {user.id}")
        if user.username == "admin_user_789":
            crud.update_user_role(db, user.id, role="admin")