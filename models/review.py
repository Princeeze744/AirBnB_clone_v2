#!/usr/bin/python3
""" Review class module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, ForeignKey
from sqlalcemy.orm import relationship
from models import storage_type


class Review(BaseModel, Base):
    """
    Review class to store review information.

    Attributes:
        __tablename__ (str): Table name for the database table.
        text (str): Column for the review text (1024 characters).
        place_id (str): Column for the place ID (foreign key to places.id).
        user_id (str): Column for the user ID (foreign key to users.id).
    """
    if storage_type == "db":
        __tablename__ = 'reviews'

        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        place = relationship(
                "Place")
    else:
        text = ""
        place_id = ""
        user_id = ""
