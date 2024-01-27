import json
import os
from flask import request, Blueprint, send_from_directory, current_app as app
from PIL import Image


picture_service = Blueprint("picture_service", __name__)


@picture_service.route("/picture/<path:path>")
def sendImage(path):
    
    CACHE_DIR = os.path.join(app.config["STORAGE_PATH"], "img", "cache")

    scaleY = request.args.get("scaley")
    scaleX = request.args.get("scalex")
    encoding = request.args.get("encoding")

    if scaleY:
        scaleY = round(float(scaleY))
    if scaleX:
        scaleX = round(float(scaleX))

    pathToGeneratedImage = generateImage(path, scaleX, scaleY, encoding)
    response = send_from_directory(CACHE_DIR, pathToGeneratedImage)

    return response


def generateImage(pathToOrig, scaleX, scaleY, encoding):
    """Generate an image with the requested scales and encoding if it doesn't already exist"""
    CACHE_DIR = os.path.join(app.config["STORAGE_PATH"], "img", "cache")
    PICTURES_DIR = os.path.join(app.config["STORAGE_PATH"], "img")

    filename, extension = os.path.splitext(os.path.basename(pathToOrig))
    flat = os.path.basename(os.path.dirname(os.path.dirname(pathToOrig)))

    # use same encoding if none is given #
    if not encoding:
        encoding = extension.strip(".")

    # fix some extensions PILLOW doesn't like #
    if encoding.lower() == "jpg":
        encoding = "jpeg"

    # generate new paths

    FILE_FORMAT = "x-{x}-y-{y}-{flat}-{fname}.{ext}"
    newFile = FILE_FORMAT.format(
        x=scaleX, y=scaleY, flat=flat, fname=filename, ext=encoding
    )
    newPath = os.path.join(CACHE_DIR, newFile)

    # check if already cache
    if os.path.exists(newPath):
        return newFile

    # create a cache dir if it doesn't already exist #
    if os.path.isfile(CACHE_DIR):
        raise OSError("Picture cache dir name is occupied by a file!")
    if not os.path.isdir(CACHE_DIR):
        os.mkdir(CACHE_DIR)

    # open image #
    image = Image.open(os.path.join(PICTURES_DIR, pathToOrig))
    # ensure sizes are valid #
    x, y = image.size
    if not scaleY:
        scaleY = y
    if not scaleX:
        scaleX = x
    scaleX = min(x, scaleX)
    scaleY = min(y, scaleY)

    # save image with new size and encoding #
    image.thumbnail((scaleX, scaleY), Image.ANTIALIAS)
    image.save(newPath, encoding)

    # return the new path #
    return newFile
