import os

from borkum.website.database import db_service
from borkum.website.database.models import ImageType

res_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'borkum', 'website', 'static')

for flat in os.listdir(os.path.join(res_path, 'img', 'apartments')):
    print(flat)
    for type in os.listdir(os.path.join(res_path, 'img', 'apartments', flat)):
        for file in  os.listdir(os.path.join(res_path, 'img', 'apartments', flat, type)):
            type = ImageType('thumbnail')
            db_service.add_flat_image(filename=file, title="", description="", type=type, flatname=flat)
