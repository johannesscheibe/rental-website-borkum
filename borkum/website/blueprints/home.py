from flask import Blueprint, render_template, current_app as app

from borkum.website.database.models import Apartment


home = Blueprint('home', __name__)

@home.route('/')
def init():
    apartments = Apartment.filter()
    return render_template("index.html", base_data=app.config['BASE_DATA'], apartments=apartments)

