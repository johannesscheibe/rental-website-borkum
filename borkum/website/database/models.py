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
    def filter(cls, **kwargs):
        return cls.query.filter_by(**kwargs)



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
    filepath = Column(String(50))
    title = Column(String(20))
    description = Column(String(100))

    __table_args__ = (UniqueConstraint("filepath"),)


class House(db.Model, BaseModel):
    __tablename__ = "house"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    displayname = Column(String(30))
    description = Column(String())

    address = Column(String(15))
    is_visible = Column(Boolean())

    # Many to One House <-> Image
    thumbnail_id = Column(Integer, ForeignKey("image.id"))
    thumbnail = relationship("Image")

   # Many to Many House <-> Image
    images = relationship("Image", secondary='house_image_mapping')

    # One to Many House <-> Apartment
    apartments = relationship("Apartment", back_populates="house")

    __table_args__ = (UniqueConstraint("name"),)

class Apartment(db.Model, BaseModel):
    __tablename__ = "apartment"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    displayname = Column(String(30))
    description = Column(String())

    # Many to One Apartment <-> House
    thumbnail_id = Column(Integer, ForeignKey("image.id"))
    thumbnail = relationship("Image")

    # Many to Many Apartment <-> Image
    images = relationship("Image", secondary='appartment_image_mapping')

    # Many to One Apartment <-> House
    house_id = Column(Integer, ForeignKey("house.id"))
    house = relationship("House", back_populates="apartments")

    # Many to Many Apartment <-> Tag
    tags = relationship("Tag", secondary='appartment_tag_mapping')

    __table_args__ = (UniqueConstraint("name"),)

appartment_image_mapping = Table(
    "appartment_image_mapping",
    db.Model.metadata,
    Column("apartment_id", ForeignKey("apartment.id")),
    Column("image_id", ForeignKey("image.id")),
)

house_image_mapping = Table(
    "house_image_mapping",
    db.Model.metadata,
    Column("house_id", ForeignKey("house.id")),
    Column("image_id", ForeignKey("image.id")),
)

appartment_tag_mapping = Table(
    "appartment_tag_mapping",
    db.Model.metadata,
    Column("apartment_id", ForeignKey("apartment.id")),
    Column("tag_id", ForeignKey("tag.id")),
)