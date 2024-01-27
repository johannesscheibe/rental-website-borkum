import json
import os
from flask import Blueprint, render_template, current_app as app

from borkum.website.database import db_service
from borkum.website.database.models import Flat, House

rental_object = Blueprint("rental_object", __name__)


@rental_object.route("/flat/<string:name>")
def init_flat_pager(name):
    flat = db_service.get_flat_by_name(name=name)
    return render_template(
        "rental_object.html", base_data=app.config["BASE_DATA"], rental_object=flat
    )


@rental_object.route("/house/<string:name>")
def init_house_page(name):
    house = db_service.filter_houses(name=name)[0]

    return render_template(
        "rental_object.html", base_data=app.config["BASE_DATA"], rental_object=house
    )
