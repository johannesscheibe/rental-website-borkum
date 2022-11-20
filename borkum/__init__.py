import json
from borkum.website import create_app
from borkum.website.database import db_service
from borkum.website.database.models import ApartmentImageMapping, House, Image


app = create_app()

@app.before_first_request
def before_first_request():
    # TODO is there a better place to store this data
    app.config['BASE_DATA'] = {}
    app.config['BASE_DATA']['contact'] = {'name': 'Ferienwohnungen Scheibe', 'street': 'Rüschenweg 46', 'city': '26188 Edewecht', 'phone': '04486 / 920167', 'email': 'vermietung.scheibe@gmail.com', 'traumfewo_name': 'traum-ferienwohnungen.de', 'traumfewo_link': 'https://www.traum-ferienwohnungen.de/objektuebersicht/scheibe/'}
    app.config['BASE_DATA']['rental_objects'] = [ { 'name': house.name, 'displayname': house.displayname, 'apartments':[ {'name': a.name, 'displayname': a.displayname} for a in house.apartments]} for  house in House.filter()]

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
        
        
    