from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from . import db

db: SQLAlchemy

class BaseModel():
    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            attr = getattr(self, c.name)
            if isinstance(attr, BaseModel):
                attr = attr.as_dict()
            d[c.name] = attr
        return d

    
    @classmethod
    def filter(cls, first=True, **kwargs):
        
        obj =  cls.query.filter_by(**kwargs)
        return obj.first() if first else obj



class TagCategory(db.Model, BaseModel):
    __tablename__ = "tag_category"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    __table_args__ = (UniqueConstraint("name"),)

class Tag(db.Model, BaseModel):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    icon = Column(String(20))
    category_id = Column(Integer, ForeignKey("tag_category.id"))

    __table_args__ = (UniqueConstraint("name"),)

class Image(db.Model, BaseModel):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True)
    filename = Column(String(50))
    title = Column(String(20))
    description = Column(String(100))

    __table_args__ = (UniqueConstraint("filename"),)


class House(db.Model, BaseModel):
    __tablename__ = "house"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    displayname = Column(String(30))
    description = Column(String())

    address = Column(String(15))
    is_visible = Column(Boolean())

    # One to Many House <-> Image
    images = relationship("HouseImageMapping", back_populates="house")

    # One to Many House <-> Apartment
    apartments = relationship("Apartment", back_populates="house")

    __table_args__ = (UniqueConstraint("name"),)

class Apartment(db.Model, BaseModel):
    __tablename__ = "apartment"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    displayname = Column(String(30))
    description = Column(String())

    # Assosiation Apartment <-> Image
    images = relationship("ApartmentImageMapping", back_populates="apartment")

    # Many to One Apartment <-> House
    house_id = Column(Integer, ForeignKey("house.id"))
    house = relationship("House", back_populates="apartments")

    # Many to Many Apartment <-> Tag
    tags = relationship("Tag", secondary='appartment_tag_mapping', backref="apartments")

    __table_args__ = (UniqueConstraint("name"),)

class ApartmentImageMapping(db.Model, BaseModel):
    __tablename__ = "apartment_image_mapping"
    apartment_id = Column(ForeignKey("apartment.id"), primary_key=True)
    image_id = Column(ForeignKey("image.id"), primary_key=True)
    
    is_thumbnail = Column(Boolean())

    apartment = relationship("Apartment", back_populates="images")
    image = relationship("Image")


class HouseImageMapping(db.Model, BaseModel):
    __tablename__ = "house_image_mapping"
    apartment_id = Column(ForeignKey("house.id"), primary_key=True)
    image_id = Column(ForeignKey("image.id"), primary_key=True)
    
    is_thumbnail = Column(Boolean())

    house = relationship("House", back_populates="images")
    image = relationship("Image")


appartment_tag_mapping = Table(
    "appartment_tag_mapping",
    db.Model.metadata,
    Column("apartment_id", ForeignKey("apartment.id")),
    Column("tag_id", ForeignKey("tag.id")),
)