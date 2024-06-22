from borkum.website.database import db_service


def get_rental_objects():
    return [
        {
            "name": house.name,
            "flats": [{"name": a.name} for a in house.flats],
        }
        for house in db_service.get_all_houses()
    ]