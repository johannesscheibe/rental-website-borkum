from pathlib import Path
import random
from flask import Blueprint, render_template, current_app as app
import os

gallery = Blueprint('gallery', __name__)

@gallery.route('/gallery')
def init():
    images = []
    for filename in os.listdir('borkum/website/static/img/gallery'):
        if filename.split(".")[-1] in ["png", "jpg", "jpeg"]:
            images.append(os.path.join('\\static\\img\\gallery', filename))
        else:
            continue

    thumbnails = []
    for filename in os.listdir('borkum/website/static/img/gallery/thumbnail'):
        if filename.split(".")[-1] in ["png", "jpg", "jpeg"]:
            thumbnails.append(('/static/img/gallery/thumbnail/' + filename))
        else:
            continue

    return render_template("gallery.html", contact=app.config['CONTACT'], images= images, thumbnail= thumbnails[random.randint(0, len(thumbnails)-1)])

