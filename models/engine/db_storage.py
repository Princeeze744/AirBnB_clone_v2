#!/usr/bin/python3
"""DBStorage Module"""
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


usr = getenv('HBNB_MYSQL_USER')
pwd = getenv('HBNB_MYSQL_PWD')
host = getenv('HBNB_MYSQL_HOST')
db = getenv('HBNB_MYSQL_DB')
env = getenv('HBNB_ENV')


class DBStorage:
    """DBStorage class"""

    __engine = None
    __session = None

    def __init__(self):
        """initialize the db storage"""
        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}:3306/{}'.format(usr, pwd, host, db),
                pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all()

    def all(self, cls=None):
        """Query all objects by class from the database"""
        if cls is not None:
            objs = self.__session.query(cls).all()
            objs_dict = {
                    f'{obj.__class__.__name__}.{obj.id}': obj
                    for obj in objs}
        else:
            objs_dict = {}
            for cls in [User, State, City, Review, Place, Amenity]:
                objs = self.__session.query(cls).all()
                objs_dict.update({
                        f'{obj.__class__.__name__}.{obj.id}': obj
                        for obj in objs})
        return objs_dict

    def new(self, obj):
        """Add the object to the current session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete the object from the current session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reloads all objects from database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine,
                expire_on_commit=False)
        self.__session = scoped_session(session_factory)
