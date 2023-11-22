#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage_type
import sqlalchemy
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Table
from sqlalchemy.orm import relationship

if storage_type == 'db':
    PlaceAmenity = Table(
            'place_amenity',
            Base.metadata,
            Column('place_id', String(60), ForeignKey('places.id'),
                   nullable=False),
            Column('amenity_id', String(60), ForeignKey('amenities.id'),
                   nullable=False))


class Place(BaseModel, Base):
    """
    class "Place" with the following Attributes:
    city_id: city id (str)
    user_id: user id (str)
    name: name of place (str)
    description: place description (str)
    number_rooms: number of rooms (int)
    number_bathrooms: number of bathrooms (int)
    max_guest: maximum number of guests (int)
    price_by_night: Price per night (int)
    latitude: latitude (flaot)
    longitude: longitude (float)
    amenity_ids: Amenity ids (str list)
    """

    if storage_type == 'db':
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=True)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship(
                'Review',
                cascade='all, delete-orphan',
                backref='place')
        amenities = relationship(
                'Amenity',
                secondary=PlaceAmenity,
                back_populates='place_amenities',
                viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def amenities(self):
            """Getter attribute"""
            from models.amenity import Amenity
            from models import storage
            self.amenity_ids = [
                    amenity.id
                    for amenity in storage.all(Amenity).values()
                    if amenity.place_id == self.id]
            return self.amenity_ids
