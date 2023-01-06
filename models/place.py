#!/usr/bin/python3
"""This is the place class"""
from os import getenv
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship, backref

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id'), primary_key=True,
                             nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'), primary_key=True,
                             nullable=False))


class Place(BaseModel, Base):
    """This is the class for Place
    Attributes:
        city_id: city id
        user_id: user id
        name: name input
        description: string of description
        number_rooms: number of room in int
        number_bathrooms: number of bathrooms in int
        max_guest: maximum guest in int
        price_by_night:: pice for a staying in int
        latitude: latitude in flaot
        longitude: longitude in float
        amenity_ids: list of Amenity ids
    """
    __tablename__ = 'places'

    city_id = Column(String(60),
                     ForeignKey("cities.id", ondelete="CASCADE"),
                     nullable=False)
    user_id = Column(String(60),
                     ForeignKey("users.id", ondelete="CASCADE"),
                     nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        reviews = relationship('Review', backref='place')
        amenities = relationship("Amenity", secondary="place_amenity",
                                 viewonly=False,
                                 back_populates="place_amenities")

    else:
        @property
        def reviews(self):
            """Review relationship with Places on File"""
            list_of_reviews = []
            for key, val in models.storage.items():
                if type(val).__name__ == "Review":
                    if val.place_id == self.id:
                        list_of_reviews.append(val)
            return (list_of_reviews)

        @property
        def amenities(self):
            """ Return list of amenities """
            aux = []
            for id in self.amenity_ids:
                key = 'Amenity.{}'.format(id)
                if key in models.storage.all().keys():
                    aux.append(models.storage.all()[key])
            return aux

        @amenities.setter
        def amenities(self, obj=None):
            if obj and type(obj).__name__ == 'Amenity':
                self.amenity_ids.append(obj.id)
