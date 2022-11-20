import json
import os
from flask import Blueprint, render_template, current_app as app

from borkum.website.database import db_service
from borkum.website.database.models import Apartment, House
apartment = Blueprint('apartment', __name__)

@apartment.route('/apartment/<string:name>')
def init_apartment_pager(name):

    apartment = Apartment.filter(name = name).first()
    tags = [tag.as_dict() for tag in apartment.tags]
    images = [img.as_dict() for img in apartment.images]
    
    res_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')

    images = []

    for filename in os.listdir(os.path.join(res_path, 'img', 'apartments', name ,'rooms')):
        if filename.split(".")[-1].lower() in ["png", "jpg", "jpeg"]:
            images.append('apartments/' + name + '/rooms/' + filename)
        else:
            continue
    filename = os.listdir(os.path.join(res_path, 'img', 'apartments', name, 'thumbnail'))[0]
    thumbnail = 'apartments/' + name + '/thumbnail/' + filename
    


    return render_template("apartment.html", base_data=app.config['BASE_DATA'], apartment=apartment, tags=tags, images=images, thumbnail=thumbnail)

@apartment.route('/house/<string:name>')
def init_house_page(name):

    house = House.filter(name=name).first()
    images = [img.as_dict() for img in house.images]
    
    res_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static')

    images = []

    for filename in os.listdir(os.path.join(res_path, 'img', 'apartments', name ,'rooms')):
        if filename.split(".")[-1].lower() in ["png", "jpg", "jpeg"]:
            images.append('apartments/' + name + '/rooms/' + filename)
        else:
            continue
    filename = os.listdir(os.path.join(res_path, 'img', 'apartments', name, 'thumbnail'))[0]
    thumbnail = 'apartments/' + name + '/thumbnail/' + filename
    
    return render_template("apartment.html", base_data=app.config['BASE_DATA'], apartment=house, tags=None, images=images, thumbnail=thumbnail)
