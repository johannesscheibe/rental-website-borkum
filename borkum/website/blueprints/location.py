import os

from flask import Blueprint, render_template
from flask import current_app as app

from borkum.website.database import db_service

from .utils import get_rental_objects

location = Blueprint('location', __name__)

@location.route('/location')
def init():
    return render_template("location.html",  rental_objects = get_rental_objects(), base_data=db_service.get_contact_information())

