import random
from flask import Blueprint, render_template, current_app as app
import os

gallery = Blueprint('gallery', __name__)

@gallery.route('/gallery')
def init():
    # Use STORAGE_PATH from config for consistency
    res_path = app.config['STORAGE_PATH']
    gallery_path = os.path.join(res_path, 'img', 'gallery')
    thumbnail_path = os.path.join(res_path, 'img', 'gallery', 'thumbnail')
    
    images = []
    if os.path.isdir(gallery_path):
        for filename in os.listdir(gallery_path):
            if filename.split(".")[-1].lower() in ["png", "jpg", "jpeg"]:
                # Use forward slashes for web paths (compatible with picture service)
                images.append('gallery/' + filename)
            else:
                continue

    thumbnails = []
    if os.path.isdir(thumbnail_path):
        for filename in os.listdir(thumbnail_path):
            if filename.split(".")[-1].lower() in ["png", "jpg", "jpeg"]:
                # Use forward slashes for web paths
                thumbnails.append('gallery/thumbnail/' + filename)
            else:
                continue
    
    # Select a random thumbnail, or use a default if none available
    selected_thumbnail = None
    if thumbnails:
        selected_thumbnail = thumbnails[random.randint(0, len(thumbnails) - 1)]
    elif images:
        # Fallback to first gallery image if no thumbnails
        selected_thumbnail = images[0]

    return render_template(
        "gallery.html", 
        contact=app.config['CONTACT'], 
        images=images, 
        thumbnail=selected_thumbnail
    )

