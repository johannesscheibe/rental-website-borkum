import os
import random
from pathlib import Path

from flask import Blueprint, render_template
from flask import current_app as app

from borkum.website.database import db_service

from .utils import get_rental_objects

gallery = Blueprint('gallery', __name__)

@gallery.route('/gallery')
def init():
    images = []
    for filename in os.listdir('borkum/website/static/images/gallery'):
        if filename.split(".")[-1] in ["png", "jpg", "jpeg"]:
            images.append(os.path.join('\\static\\images\\gallery', filename))
        else:
            continue

    thumbnails = []
    for filename in os.listdir('borkum/website/static/images/gallery/thumbnail'):
        if filename.split(".")[-1] in ["png", "jpg", "jpeg"]:
            thumbnails.append(('/static/images/gallery/thumbnail/' + filename))
        else:
            continue

    return render_template("gallery.html", rental_objects = get_rental_objects(), base_data=db_service.get_contact_information, images= images, thumbnail= thumbnails[random.randint(0, len(thumbnails)-1)])

