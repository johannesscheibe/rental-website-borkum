from flask import Blueprint, render_template
from flask import current_app as app

from borkum.website.database import db_service

from .utils import get_rental_objects

home = Blueprint("home", __name__)


@home.route("/")
def init():
    flats = db_service.filter_flats()
    return render_template("index.html", rental_objects = get_rental_objects(), base_data=db_service.get_contact_information(), flats=flats)
