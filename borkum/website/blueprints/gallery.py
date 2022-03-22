from pathlib import Path
import random
from flask import Blueprint, render_template
import os

gallery = Blueprint('gallery', __name__)

@gallery.route('/gallery')
def init():
    images = []
    for filename in os.listdir('borkum/website/static/img/Gallery'):
        if filename.split(".")[-1] in ["png", "jpg", "jpeg"]:
            images.append(os.path.join('\\static\\img\\Gallery', filename))
        else:
            continue

    thumbnails = []
    for filename in os.listdir('borkum/website/static/img/Gallery/Thumbnail'):
        if filename.split(".")[-1] in ["png", "jpg", "jpeg"]:
            thumbnails.append(('/static/img/Gallery/Thumbnail/' + filename))
        else:
            continue

    return render_template("gallery.html", images= images, thumbnail= thumbnails[random.randint(0, len(thumbnails)-1)])

