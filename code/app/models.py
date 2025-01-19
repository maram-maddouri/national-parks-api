from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


Base = declarative_base()


class Park(Base):
    __tablename__ = "parks"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    description = Column(String)
    images = Column(String)
    created_at = Column(String, server_default=func.now())
    updated_at = Column(String, server_default=func.now(), onupdate=func.now())
    species = relationship("Species", back_populates="park")

    
class Species(Base):
    __tablename__ = "species"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    scientific_name = Column(String)
    park_id = Column(Integer, ForeignKey("parks.id"))
    description = Column(String)
    image = Column(String)
    created_at = Column(String, server_default=func.now())
    updated_at = Column(String, server_default=func.now(), onupdate=func.now())

    park = relationship("Park", back_populates="species")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="visitor")  # Default role for new users
    created_at = Column(String, server_default=func.now())
    updated_at = Column(String, server_default=func.now(), onupdate=func.now())