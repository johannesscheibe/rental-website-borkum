from flask import Blueprint, render_template
import os

gallery = Blueprint('gallery', __name__)

@gallery.route('/gallery')
def init():
    images = []
    for filename in os.listdir('borkum/website/static/img/Gallery'):
        if filename.split(".")[-1] in ["png", "jpg", "jpeg"]:
            print(filename)
            images.append(os.path.join('\\static\\img\\Gallery', filename))
        else:
            continue
    return render_template("gallery.html", images= images)

