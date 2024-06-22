import os

from flask import Blueprint, render_template
from flask import current_app as app

from borkum.website.database import db_service

from .utils import get_rental_objects

legal_information = Blueprint('legal_information', __name__)

@legal_information.route('/impressum')
def impressum():
    return render_template("impressum.html",  rental_objects = get_rental_objects(), base_data=db_service.get_contact_information())


@legal_information.route('/privacy')
def privacy():
    return render_template("privacy.html",  rental_objects = get_rental_objects(), base_data=db_service.get_contact_information())


@legal_information.route('/terms_of_use')
def terms_of_use():
    return render_template("terms_of_use.html",  rental_objects = get_rental_objects(), base_data=db_service.get_contact_information())

