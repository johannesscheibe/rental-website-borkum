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
