from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.db import get_db
from app.auth import get_current_user, get_admin_user

router = APIRouter(prefix="/species", tags=["species"])


@router.get("/", response_model=List[schemas.Species])
def read_species(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    species = crud.get_species(db, skip=skip, limit=limit)
    return species


@router.get("/{species_id}", response_model=schemas.Species)
def read_species_by_id(species_id: int, db: Session = Depends(get_db)):
    db_species = crud.get_species_by_id(db, species_id=species_id)
    if db_species is None:
        raise HTTPException(status_code=404, detail="Species not found")
    return db_species


@router.get("/parks/{park_id}/species", response_model=List[schemas.Species])
def read_species_by_park(park_id: int, db: Session = Depends(get_db)):
    species = crud.get_species_by_park(db, park_id=park_id)
    return species


@router.post("/", response_model=schemas.Species, status_code=status.HTTP_201_CREATED)
def create_species(
    species: schemas.SpeciesCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user),
):
    return crud.create_species(db, species)


@router.put("/{species_id}", response_model=schemas.Species)
def update_species(
    species_id: int,
    species: schemas.SpeciesCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user),
):
    db_species = crud.update_species(db, species_id=species_id, species=species)
    if db_species is None:
        raise HTTPException(status_code=404, detail="Species not found")
    return db_species


@router.delete("/{species_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_species(
    species_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_admin_user),
):
    if not crud.delete_species(db, species_id=species_id):
        raise HTTPException(status_code=404, detail="Species not found")
    return None