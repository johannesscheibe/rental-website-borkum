from flask import Blueprint, render_template, current_app as app

from borkum.website.database import db_service


home = Blueprint("home", __name__)


@home.route("/")
def init():
    flats = db_service.filter_flats()
    return render_template("index.html", base_data=app.config["BASE_DATA"], flats=flats)
