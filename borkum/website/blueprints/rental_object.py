import json
import os

from flask import Blueprint, render_template
from flask import current_app as app

from borkum.website.database import db_service

from .utils import get_rental_objects

rental_object = Blueprint("rental_object", __name__)


@rental_object.route("/flat/<string:name>")
def init_flat_pager(name):
    flat = db_service.get_flat_by_name(name=name)
    return render_template(
        "rental_object.html", rental_objects = get_rental_objects(), base_data=db_service.get_contact_information(), rental_object=flat
    )


@rental_object.route("/house/<string:name>")
def init_house_page(name):
    house = db_service.filter_houses(name=name)[0]

    return render_template(
        "rental_object.html", rental_objects = get_rental_objects(), base_data=db_service.get_contact_information(), rental_object=house
    )
