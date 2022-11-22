import json
import os
from flask import Blueprint, render_template, current_app as app

from borkum.website.database import db_service
from borkum.website.database.models import Apartment, House

rental_object = Blueprint('rental_object', __name__)

@rental_object.route('/apartment/<string:name>')
def init_apartment_pager(name):

    apartment = Apartment.filter(name = name).first()
    return render_template("rental_object.html", base_data=app.config['BASE_DATA'], rental_object=apartment)

@rental_object.route('/house/<string:name>')
def init_house_page(name):

    house = House.filter(name=name).first()

    return render_template("rental_object.html", base_data=app.config['BASE_DATA'], rental_object=house)
