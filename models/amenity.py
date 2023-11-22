#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage_type
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

if storage_type == 'db':
    from models.place import PlaceAmenity


class Amenity(BaseModel, Base):
    """
    Amenity class
    """
    if storage_type == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship(
                'Place',
                secondary=PlaceAmenity,
                back_populates='amenities')
    else:
        name = ""
