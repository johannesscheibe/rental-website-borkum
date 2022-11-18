import json
from borkum.website import create_app
from borkum.website.database import db_service
from borkum.website.database.models import ApartmentImages, Image


app = create_app()

@app.cli.command('seed')
def seed():
    data = json.load(open("/Users/johannesscheibe/Documents/Projects/borkum-website/scripts/db_objects.json"))

    # seed tags
    for tag in data["tags"]:
        category = db_service.add_tag_category(name=tag['category'])
        
        db_service.add_tag(name=tag['name'], icon=tag['icon'], category_id = category.id)
        
    # seed houses
    for obj in data["houses"]:
        house = db_service.add_house(**obj)
        print(house.as_dict())
        
    # seed apartments
    for obj in data["apartments"]:
        print(obj)
        apartment = db_service.add_apartment(**obj)
        print(apartment.as_dict())
        print(apartment.tags)
        print(apartment.images)
        
        
    