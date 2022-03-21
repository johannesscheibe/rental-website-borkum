from flask import Blueprint, render_template
import os

location = Blueprint('location', __name__)

@location.route('/location')
def init():
    return render_template("location.html")

