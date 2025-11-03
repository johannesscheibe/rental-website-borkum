import json
import os
from flask import request, Blueprint, send_from_directory, current_app as app, abort
from PIL import Image


picture_service = Blueprint('picture_service', __name__)


def validate_image_path(path):
    """
    Validate that the image path is safe and within allowed directories.
    Prevents path traversal attacks.
    
    Returns:
        tuple: (is_valid, normalized_path) or (False, None) if invalid
    """
    if not path:
        return False, None
    
    # Normalize the path to resolve any directory traversal attempts
    normalized_path = os.path.normpath(path)
    
    # Check for directory traversal attempts (..) or absolute paths
    if '..' in normalized_path or os.path.isabs(normalized_path):
        return False, None
    
    # Ensure the path uses forward slashes (web path format)
    # and doesn't contain backslashes (Windows path injection)
    if '\\' in path or path.startswith('/'):
        return False, None
    
    # Get the allowed base directory
    PICTURES_DIR = os.path.join(app.config['STORAGE_PATH'], 'img')
    PICTURES_DIR = os.path.abspath(PICTURES_DIR)  # Ensure absolute path
    
    # Construct the full path
    full_path = os.path.join(PICTURES_DIR, normalized_path)
    full_path = os.path.abspath(full_path)  # Resolve any remaining issues
    
    # Verify the resolved path is within the allowed directory
    # This prevents accessing files outside PICTURES_DIR
    try:
        if not full_path.startswith(PICTURES_DIR):
            return False, None
    except (ValueError, AttributeError):
        # Handle edge cases where paths can't be compared
        return False, None
    
    # Verify the file exists
    if not os.path.exists(full_path):
        return False, None
    
    # Verify it's actually a file, not a directory
    if not os.path.isfile(full_path):
        return False, None
    
    # Check file extension is an allowed image type
    allowed_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
    _, ext = os.path.splitext(full_path)
    if ext.lower() not in allowed_extensions:
        return False, None
    
    return True, normalized_path


@picture_service.route("/picture/<path:path>")
def sendImage(path):
    """
    Serve images with optional scaling and encoding.
    Path is validated to prevent directory traversal attacks.
    """
    # Validate the path
    is_valid, safe_path = validate_image_path(path)
    if not is_valid:
        abort(404)  # Return 404 for invalid paths (don't reveal they're blocked)
    
    CACHE_DIR = os.path.join(app.config['STORAGE_PATH'],  'img', 'cache')
    
    scaleY = request.args.get("scaley")
    scaleX = request.args.get("scalex")
    encoding = request.args.get("encoding")
    
    if scaleY:
        scaleY = round(float(scaleY))
    if scaleX:
        scaleX = round(float(scaleX))
    
    try:
        pathToGeneratedImage = generateImage(safe_path, scaleX, scaleY, encoding)
        response = send_from_directory(CACHE_DIR, pathToGeneratedImage)
        return response
    except (OSError, IOError, Image.UnidentifiedImageError):
        # Handle file errors gracefully
        abort(404)


def generateImage(pathToOrig, scaleX, scaleY, encoding):
    """
    Generate an image with the requested scales and encoding if it doesn't already exist.
    
    Args:
        pathToOrig: Safe, validated relative path to the original image
        scaleX: Target width (or None for original)
        scaleY: Target height (or None for original)
        encoding: Target encoding format (or None for original)
    
    Returns:
        str: Filename of the generated/cached image
    """
    CACHE_DIR = os.path.join(app.config['STORAGE_PATH'], 'img', 'cache')
    PICTURES_DIR = os.path.join(app.config['STORAGE_PATH'], 'img')
    PICTURES_DIR = os.path.abspath(PICTURES_DIR)

    # Get the original image path (already validated)
    original_image_path = os.path.join(PICTURES_DIR, pathToOrig)
    original_image_path = os.path.abspath(original_image_path)
    
    # Double-check the path is still valid (defense in depth)
    if not original_image_path.startswith(PICTURES_DIR):
        raise ValueError("Invalid image path")
    
    if not os.path.isfile(original_image_path):
        raise FileNotFoundError("Image not found")
    
    # Extract filename and extension safely
    filename, extension = os.path.splitext(os.path.basename(pathToOrig))
    
    # Extract apartment name from path structure (e.g., "apartments/baltrum/thumbnail/file.jpg")
    # Handle different path structures (apartments/, gallery/, header.png, etc.)
    path_parts = pathToOrig.split(os.sep)
    if len(path_parts) >= 2 and path_parts[0] == 'apartments':
        apartment = path_parts[1]  # e.g., "baltrum"
    else:
        # For gallery, header, or other top-level images, use directory name
        apartment = path_parts[0] if path_parts else 'misc'

    # use same encoding if none is given
    if not encoding:
        encoding = extension.strip(".")

    # fix some extensions PILLOW doesn't like
    if encoding.lower() == "jpg":
        encoding = "jpeg"
    
    # Sanitize filename and apartment name for use in cache filename
    # Remove any potentially dangerous characters
    filename = "".join(c for c in filename if c.isalnum() or c in ('-', '_', '.'))
    apartment = "".join(c for c in apartment if c.isalnum() or c in ('-', '_'))
    
    # generate new paths
    FILE_FORMAT = "x-{x}-y-{y}-{apartment}-{fname}.{ext}"
    newFile = FILE_FORMAT.format(x=scaleX or 0, y=scaleY or 0, apartment=apartment, fname=filename, ext=encoding)
    newPath = os.path.join(CACHE_DIR, newFile)
    
    # Ensure cache filename doesn't contain path traversal
    newPath = os.path.abspath(newPath)
    if not newPath.startswith(os.path.abspath(CACHE_DIR)):
        raise ValueError("Invalid cache path generated")
    
    # check if already cached
    if os.path.exists(newPath):
        return newFile
 
    # create a cache dir if it doesn't already exist
    if os.path.isfile(CACHE_DIR):
        raise OSError("Picture cache dir name is occupied by a file!")
    if not os.path.isdir(CACHE_DIR):
        os.makedirs(CACHE_DIR, exist_ok=True)

    # open image
    image = Image.open(original_image_path)
    
    # ensure sizes are valid
    x, y = image.size
    if not scaleY:
        scaleY = y
    if not scaleX:
        scaleX = x
    scaleX = min(x, scaleX)
    scaleY = min(y, scaleY)

    # save image with new size and encoding #
    image.thumbnail((scaleX, scaleY), Image.LANCZOS)
    image.save(newPath, encoding)

    # return the new path
    return newFile