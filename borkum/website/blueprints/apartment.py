import json
import os
from flask import Blueprint, render_template, current_app as app

from borkum.website.database import db_service
from borkum.website.database.models import Apartment, House
apartment = Blueprint('apartment', __name__)

@apartment.route('/apartment/<string:fewo>')
def init(fewo):

    apartment = Apartment.filter(name = fewo).first()
    tags = [tag.as_dict() for tag in apartment.tags]
    images = [img.as_dict() for img in apartment.images]
    
    res_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')

    images = []

    for filename in os.listdir(os.path.join(res_path, 'img', 'apartments', fewo ,'rooms')):
        if filename.split(".")[-1].lower() in ["png", "jpg", "jpeg"]:
            images.append('apartments/' + fewo + '/rooms/' + filename)
        else:
            continue
    filename = os.listdir(os.path.join(res_path, 'img', 'apartments', fewo, 'thumbnail'))[0]
    thumbnail = 'apartments/' + fewo + '/thumbnail/' + filename
    


    return render_template("apartment.html", base_data=app.config['BASE_DATA'], apartment=apartment, tags=tags, images=images, thumbnail=thumbnail)

