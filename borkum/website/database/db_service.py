from typing import List
from .models import *




def add_apartment(name:str, description:str, tags: List, house: House, thumbnail: Image, images: list[Image]) -> Apartment:

    apartment = Apartment.query.filter_by(name=name).first()
    if apartment:
        return None
    
    new_apartment = Apartment(name=name, description=description, house_id=house.id, thumbnail_id=thumbnail.id)
    db.session.add(new_apartment)

    for image in images:
        new_apartment.images.append(image)
    
    for tag in tags:
        new_apartment.tags.append(tag)

    db.session.commit()

    return new_apartment

