import glob
import json
import os
from pathlib import Path
import uuid
from borkum.website import create_app
from borkum.website.database import db_service, db
from borkum.website.database.models import Apartment, House, Image
import PIL

app = create_app()

# TODO is there a better place to store this data
@app.before_request
def get_rental_objects():
    app.config['BASE_DATA']['rental_objects'] = [ { 'name': house.name, 'displayname': house.displayname, 'is_visible': house.is_visible, 'apartments':[ {'name': a.name, 'displayname': a.displayname} for a in house.apartments]} for  house in House.filter()]

@app.before_first_request
def before_first_request():
    app.config['BASE_DATA'] = {}
    app.config['BASE_DATA']['contact'] = {'name': 'Ferienwohnungen Scheibe', 'street': 'Rüschenweg 46', 'city': '26188 Edewecht', 'phone': '04486 / 920167', 'email': 'vermietung.scheibe@gmail.com', 'traumfewo_name': 'traum-ferienwohnungen.de', 'traumfewo_link': 'https://www.traum-ferienwohnungen.de/objektuebersicht/scheibe/'}
    

@app.cli.command('seed')
def seed():
    data = json.load(open("scripts/db_objects.json"))

    # seed tags
    for tag in data["tags"]:
        category = db_service.add_tag_category(name=tag['category'])
        
        db_service.add_tag(name=tag['name'], icon=tag['icon'], category_id = category.id)
        
    # seed houses
    for obj in data["houses"]:
        house = db_service.add_house(**obj)
        print(house.to_dict())
        
    # seed apartments
    for obj in data["apartments"]:
        object_name = db_service.add_apartment(**obj)

    # seed images
    for path in glob.glob("scripts/images/apartments/*/rooms/*.*"):
        object_name, _, file_name = path.split("/")[-3:]
        dir = Path("borkum/website/static/img") 
        os.makedirs(dir / ("apartments/" + object_name), exist_ok=True)

        img = PIL.Image.open(path)
        img = img.convert('RGB')

        id = uuid.uuid4()
        fn = Path("apartments/" + object_name) / (str(id) + '.jpg')
        

        img.save(dir / fn)

        image = db_service.add_image(filepath=str(fn), title=" ".join(file_name.split(".")[0].split("-")[1:]), description="")
        apartment = Apartment.filter(name=object_name).first()
        if apartment:
            apartment.images.append(image)
            db.session.commit()
        else:
            house = House.filter(name=object_name).first()
            if house:
                house.images.append(image)
                db.session.commit()
                

        
        
    