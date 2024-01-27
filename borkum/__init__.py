import glob
import json
import os
from pathlib import Path
import uuid
from borkum.website import create_app
from borkum.website.database import db_service
from PIL import Image

app = create_app()


# TODO is there a better place to store this data
@app.before_request
def get_rental_objects():
    app.config["BASE_DATA"] = {}
    app.config["BASE_DATA"]["rental_objects"] = [
        {
            "name": house.name,
            "flats": [{"name": a.name} for a in house.flats],
        }
        for house in db_service.get_all_houses()
    ]
    app.config["BASE_DATA"]["contact"] = {
        "name": "Ferienwohnungen Scheibe",
        "street": "Rüschenweg 46",
        "city": "26188 Edewecht",
        "phone": "04486 / 920167",
        "email": "vermietung.scheibe@gmail.com",
        "traumfewo_name": "traum-ferienwohnungen.de",
        "traumfewo_link": "https://www.traum-ferienwohnungen.de/objektuebersicht/scheibe/",
    }
