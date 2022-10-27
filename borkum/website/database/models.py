import json

from flask_sqlalchemy import SQLAlchemy
from . import db

import enum
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship
from flask import current_app as app

db: SQLAlchemy

class Base():
    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            attr = getattr(self, c.name)
            if isinstance(attr, Base):
                attr = attr.as_dict()
            d[c.name] = attr
        return d


image_mapping = db.Table(
    "Image Mapping",
    db.Column("object_id", db.ForeignKey("RentalObject.id")),
    db.Column("image_id", db.ForeignKey("Image.id")),
)

tag_mapping = db.Table(
    "Tag Mapping",
    db.Column("flat_id", db.ForeignKey("Apartment.id")),
    db.Column("tag_id", db.ForeignKey("Tag.id")),
)

class RentalObject(Base):
    __tablename__ = "RentalObject"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.String())

    thumbnail_id = db.Column(db.Integer, db.ForeignKey("Image.id"))
    thumbnail = relationship("Image") # Many to One Relationship
    
    images = relationship("Image", secondary=image_mapping) # Many to Many Relationship

    __mapper_args__ = {'polymorphic_on': building_type}

class House(RentalObject, db.Model):
    __mapper_args__ = {'polymorphic_identity': 'house'}
    
    address = db.Column(db.String(15))
    visible = db.Column(db.Boolean())

    __table_args__ = (UniqueConstraint('name'),)

class Apartment(RentalObject, db.Model):
    __mapper_args__ = {'polymorphic_identity': 'apartment'}



    house_id = db.Column(db.Integer, db.ForeignKey('House.id'))
    house = relationship('House')  # Many to One Relationship

    tags = relationship("Tag", secondary=tag_mapping) # Many to Many Relationship
    
    __table_args__ = (UniqueConstraint('name'),)

class Tag(Base, db.Model):
    __tablename__ = "Tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    icon = db.Column(db.String(20))
    # category = db.Column(db.String(20))

class Image(Base, db.Model):
    __tablename__ = "Image"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    title = db.Column(db.String(20))
    description = db.Column(db.String(100))

    __table_args__ = (UniqueConstraint('filename'),)

