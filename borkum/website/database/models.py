import json
from . import db

import enum
from sqlalchemy import Enum, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from flask import current_app as app

class Base():
    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            attr = getattr(self, c.name)
            if isinstance(attr, Base):
                attr = attr.as_dict()
            d[c.name] = attr
        return d

class ImageType(enum.Enum):
    thumbnail = 'thumbnail'
    room = 'room_image'

class Flat(Base, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String())
    _properties= db.Column('properties', db.String(), default='[]')
    __table_args__ = (UniqueConstraint('name'),)
    
    @hybrid_property
    def properties(self):
        return json.loads(self._properties)

    @properties.setter
    def properties(self, properties):
        self._properties = json.dumps(properties)

class FlatImage(Base, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    title = db.Column(db.String(20))
    description = db.Column(db.String(100))
    type = db.Column(Enum(ImageType))
    flat_id = db.Column(db.Integer, db.ForeignKey('flat.id'))
    __table_args__ = (UniqueConstraint('filename'),)

class Properties(Base, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    icon = db.Column(db.String(15))

