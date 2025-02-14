#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models import storage_type


class User(BaseModel, Base):
    """
    This class defines a user with the following
    attributes:
    email: email address
    password: password for user login
    first_name: first name
    last_name: last name
    """
    if storage_type == "db":
        __tablename__ = 'users'

        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)

        places = relationship('Place', cascade='all, delete-orphan',
                              backref='user')
        reviews = relationship("Review", cascade='all, delete, delete-orphan',
                               backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
