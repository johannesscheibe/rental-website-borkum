from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship

from . import db


class House(db.Model):
    __tablename__ = "houses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    address = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    images = relationship("HouseImage", back_populates="house", lazy=True)

    flats = relationship("Flat", back_populates="house", lazy=True)

    def __repr__(self):
        return f"House('{self.name}', '{self.address}')"


class Flat(db.Model):
    __tablename__ = "flats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    tags = db.relationship("Tag", secondary="flat_tag_association", backref="flats")

    images = relationship("FlatImage", back_populates="flat", lazy=True)

    house_id = Column(Integer, ForeignKey("houses.id"), nullable=False)
    house = relationship("House", back_populates="flats")

    def __repr__(self):
        return f"Flat('{self.name}')"


class FlatImage(db.Model):
    __tablename__ = "flat_images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(255), nullable=False, unique=True)
    title = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)

    flat_id = Column(Integer, ForeignKey("flats.id"), nullable=False)
    flat = relationship("Flat", back_populates="images")

    def __repr__(self):
        return f"FlatImage('{self.image_url}')"


class HouseImage(db.Model):
    __tablename__ = "house_images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(255), nullable=False, unique=True)
    title = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)

    house_id = Column(Integer, ForeignKey("houses.id"), nullable=False)
    house = relationship("House", back_populates="images")

    def __repr__(self):
        return f"HouseImage('{self.image_url}')"


class Tag(db.Model):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    category_id = Column(
        Integer,
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    category = relationship("Category", back_populates="tags")

    def __repr__(self):
        return f"Tag('{self.name}')"


class Category(db.Model):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    tags = relationship("Tag", back_populates="category")

    def __repr__(self):
        return f"Category('{self.name}')"


# Many-to-many relationship
flat_tag_association = Table(
    "flat_tag_association",
    db.Model.metadata,
    Column(
        "flat_id", Integer, ForeignKey("flats.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    ),
)
