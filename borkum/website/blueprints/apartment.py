import json
import os
from flask import Blueprint, render_template

apartment = Blueprint('apartment', __name__)

@apartment.route('/apartment/<string:fewo>')
def init(fewo):
    data = json.load(open('borkum/website/static/content/apartments.json', encoding='utf-8'))
    images = []
    for filename in os.listdir('borkum/website/static/img/Apartments/' + fewo + '/rooms'):
        if filename.split(".")[-1] in ["png", "jpg", "jpeg"]:
            images.append(os.path.join('\\static\\img\\Apartments\\' + fewo + '\\rooms', filename))
        else:
            continue
    filename = os.listdir('borkum/website/static/img/apartments/' + fewo + '/thumbnail')[0]
    thumbnail = '/static/img/apartments/' + fewo + '/thumbnail/' + filename
    return render_template("apartment.html", info=data[fewo], images=images, thumbnail=thumbnail)

