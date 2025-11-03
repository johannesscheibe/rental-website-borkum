import os


class Config(object):
    SECRET_KEY ='j4td#+s3dHtzX'
    STORAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "borkum", "website", "static")

    CONTACT = {
        "name": "Ferienwohnungen Scheibe",
        "street": "Greune-Stee-Weg 43",
        "city": "26757 Borkum",
        "phone": "04486 / 920167",
        "email": "vermietung.scheibe@gmail.com",
        "traumfewo_name": "traum-ferienwohnungen.de",
        "traumfewo_link": "https://www.traum-ferienwohnungen.de/objektuebersicht/scheibe/",

    }
