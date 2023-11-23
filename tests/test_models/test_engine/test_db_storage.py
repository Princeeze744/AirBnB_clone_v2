#!/usr/bin/python3
"""
This module defines unnittests for models/engine/db_storage.py.
"""
import pep8
import models
import MySQLdb
import unittest
from os import getenv
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.engine.base import Engine


class TestDBStorage(unittest.TestCase):
    """Test cases for DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """DBStorage testing setup.
        Instantiate new DBStorage and fill it with test data.
        """
        if type(models.storage) == DBStorage:
            cls.storage = DBStorage()
            cls.setup_test_data(cls.storage)

    @classmethod
    def setup_test_data(cls, storage):
        """Helper method to set up test data."""
        Base.metadata.create_all(storage._DBStorage__engine)
        Session = sessionmaker(bind=storage._DBStorage__engine)
        storage._DBStorage__session = Session()

        cls.state = State(name="California")
        cls.city = City(name="San_Jose", state_id=cls.state.id)
        cls.user = User(email="poppy@alxschool.com", password="betty")
        cls.place = Place(
            city_id=cls.city.id,
            user_id=cls.user.id,
            name="School"
        )
        cls.amenity = Amenity(
            name="Wifi"
        )
        cls.review = Review(
            place_id=cls.place.id,
            user_id=cls.user.id,
            text="stellar"
        )

        objs_to_add = [
            cls.state,
            cls.city,
            cls.user,
            cls.place,
            cls.amenity,
            cls.review
        ]

        for obj in objs_to_add:
            storage._DBStorage__session.add(obj)

        storage._DBStorage__session.commit()

    @classmethod
    def tearDownClass(cls):
        """Tear down the DBStorage testing setup."""
        if type(models.storage) == DBStorage:
            cls.cleanup_test_data(cls.storage)

    @classmethod
    def cleanup_test_data(cls, storage):
        """Helper method to clean up test data."""
        objs_to_delete = [
            cls.state,
            cls.city,
            cls.user,
            cls.place,
            cls.amenity,
            cls.review
        ]

        for obj in objs_to_delete:
            storage._DBStorage__session.delete(obj)

        storage._DBStorage__session.commit()

        storage._DBStorage__session.close()

        Base.metadata.drop_all(storage._DBStorage__engine)

    def test_pep8_compliance(self):
        """
        Test to check for pep8 style guide
        conformance of db_storage.py.
        """
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings_presence(self):
        """
        test to check for the existence of
        docstrings class and method files.
        """
        self.assertIsNotNone(DBStorage.__doc__)
        self.assertIsNotNone(DBStorage.__init__.__doc__)
        self.assertIsNotNone(DBStorage.all.__doc__)
        self.assertIsNotNone(DBStorage.new.__doc__)
        self.assertIsNotNone(DBStorage.save.__doc__)
        self.assertIsNotNone(DBStorage.delete.__doc__)
        self.assertIsNotNone(DBStorage.reload.__doc__)

    @unittest.skipIf(type(models.storage) != DBStorage,
                     "not testing for DBStorage")
    def test_all_with_class(self):
        """test the "all" method with specific class object"""
        state_obj = State(name="California")
        city_obj = City(name="Los Angeles")
        user_obj = User(name="Myles Meyer")

        self.storage._DBStorage__session.add(state_obj)
        self.storage._DBStorage__session.add(city_obj)
        self.storage._DBStorage__session.add(user_obj)
        self.storage.save()

        result = self.storage.all(State)
        self.assertIsInstance(result, dict)
        self.assertIn(f'State.{state_obj.id}', result)
        self.assertEqual(result[f'State.{state_obj.id}'], state_obj)

    @unittest.skipIf(type(models.storage) != DBStorage,
                     "not testing for DBStorage")
    def test_all_without_class(self):
        """test the "all" method with specific class"""
        state_obj = State(name="California")
        city_obj = City(name="Los Angeles")
        user_obj = User(name="Myles Meyer")

        self.storage._DBStorage__session.add(state_obj)
        self.storage._DBStorage__session.add(city_obj)
        self.storage._DBStorage__session.add(user_obj)
        self.storage.save()

        result = self.storage.all()
        self.assertIsInstance(result, dict)
        self.assertIn(f'State.{state_obj.id}', result)
        self.assertEqual(result[f'State.{state_obj.id}'], state_obj)
        self.assertIn(f'City.{city_obj.id}', result)
        self.assertEqual(result[f'City.{city_obj.id}'], city_obj)
        self.assertIn(f'User.{user_obj.id}', result)
        self.assertEqual(result[f'User.{user_obj.id}'], user_obj)

    @unittest.skipIf(type(models.storage) != DBStorage,
                     "not testing for DBStorage")
    def test_new(self):
        """Test to create a new object"""
        obj = State(name="Texas")
        self.storage.new(obj)
        self.assertIn(obj, self.storage._DBStorage__session.new)

    @unittest.skipIf(type(models.storage) != DBStorage,
                     "not testing for DBStorage")
    def test_save(self):
        """Test to save object in the database."""
        obj = State(name="California")
        self.storage._DBStorage__session.add(obj)
        self.storage.save()
        with MySQLdb.connect(
            user="hbnb_test",
            passwd="hbnb_test_pwd",
            db="hbnb_test_db"
        ) as db:
            with db.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM states WHERE BINARY name = 'California'"
                )
                query = cursor.fetchall()
                self.assertEqual(1, len(query))
                self.assertEqual(obj.id, query[0][0])

    @unittest.skipIf(type(models.storage) != DBStorage,
                     "not testing for DBStorage")
    def test_delete(self):
        """Test to delete an object"""
        obj = State(name="Texas")
        self.storage._DBStorage__session.add(obj)
        self.storage._DBStorage__session.commit()
        self.storage.delete(obj)
        self.assertIn(obj, self.storage._DBStorage__session.deleted)

    @unittest.skipIf(type(models.storage) != DBStorage,
                     "not testing for DBStorage")
    def test_reload(self):
        """
        Test to check if a session is
        changed when the reload() is called
        """
        # Store the original database session
        prev_session = self.storage._DBStorage__session

        # Reload the database session
        self.storage.reload()

        # Check if the reloaded session is an instance of the Session class
        self.assertIsInstance(self.storage._DBStorage__session, Session)

        # Ensure that the reloaded session is not the same as the original one
        self.assertNotEqual(prev_session, self.storage._DBStorage__session)

        # Close the reloaded session for proper resource management
        self.storage._DBStorage__session.close()

        # Restore the original session to clean up the test environment
        self.storage._DBStorage__session = prev_session


if __name__ == "__main__":
    unittest.main()
