from flask import Blueprint, render_template, current_app as app
import os

location = Blueprint('location', __name__)

@location.route('/location')
def init():
    return render_template("location.html",  contact=app.config['CONTACT'],)

