#!/usr/bin/python3

import unittest
import models
from models.base_model import BaseModel, Base
from models.user import User
from models.review import Review
from models.amenity import Amenity
from models.state import State
from models.place import Place
from models.city import City
import os
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker


@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                 "only testing db")
class test_DBStorage(unittest.TestCase):

    def test_State(self):
        """ Check if loads name"""
        state = State(name="Carl")
        if state.id in models.storage.all():
            self.assertTrue(state.name, "Carl")

    def test_City(self):
        """ Check if loads name """
        city = City(name="Bogota")
        if city.id in models.storage.all():
            self.assertTrue(city.name, "Bogota")

    def test_Place(self):
        """ Checks if leads name and numer """
        place = Place(name="Hotel", number_rooms=4)
        if place.id in models.storage.all():
            self.assertTrue(place.number_rooms, 4)
            self.assertTrue(place.name, "Hotel")

    def test_User(self):
        """ Check if loads name """
        user = User(name="926")
        if user.id in models.storage.all():
            self.assertTrue(user.name, "926")

    def test_Amenity(self):
        """ Check if loads name """
        amenity = Amenity(name="Wifi")
        if amenity.id in models.storage.all():
            self.assertTrue(amenity.name, "Wifi")

    def test_Review(self):
        """ Tests if leads text """
        review = Review(text="Very_good_place")
        if review.id in models.storage.all():
            self.assertTrue(review.text, "Very_good_place")

    def teardown(self):
        self.session.close()
        self.session.rollback()
