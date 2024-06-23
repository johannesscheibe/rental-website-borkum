import os
from tempfile import TemporaryDirectory
import uuid
from pathlib import Path
from typing import Literal

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
)
from flask import (
    current_app as app,
)

from borkum.website.database import db_service

from .utils import get_rental_objects
from .utils.forms import FlatForm, HouseForm, NewImageForm, UpdateImageForm
from PIL import Image

admin = Blueprint("admin", __name__)


@admin.route("/admin", methods=["GET"])
def admin_page():
    return render_template(
        "admin/index.html",
        rental_objects=get_rental_objects(),
        base_data=db_service.get_contact_information(),
    )


@admin.route("/admin/flats", methods=["GET"])
def flat_overview():
    flats = db_service.get_all_flats()
    return render_template(
        "admin/flat_overview.html",
        rental_objects=get_rental_objects(),
        base_data=db_service.get_contact_information(),
        flats=flats,
    )


@admin.route("/admin/flats/add", methods=["GET", "POST"])
@admin.route("/admin/flat/<string:flat_id>/update", methods=["GET", "POST"])
def flat_form(flat_id: str | None = None):
    form = FlatForm()

    flat = db_service.get_flat_by_id(flat_id) if flat_id is not None else None

    if request.method == "POST" and form.validate_on_submit():
        data = {
            "name": request.form.get("name"),
            "description": request.form.get("description"),
            "house_id": request.form.get("house")
            if request.form.get("house")
            else None,
            "tags": [
                db_service.get_tag_by_id(int(t)) for t in request.form.getlist("tags")
            ],
        }
        if flat is not None:
            flat = db_service.update_flat(flat.id, **data)
        else:
            flat = db_service.create_flat(**data)

        return redirect(url_for("admin.flat_overview"))

    form.tags.choices = [(tag.id, tag.name) for tag in db_service.get_all_tags()]
    form.house.choices = [
        (house.id, house.name) for house in db_service.get_all_houses()
    ]

    if flat is not None:
        data = {
            "name": flat.name,
            "description": flat.description,
            "house": flat.house.id if flat.house else None,
            "tags": [tag.id for tag in flat.tags],
        }
        form.process(data=data)

    return render_template(
        "admin/flat_form.html",
        form=form,
        rental_objects=get_rental_objects(),
        base_data=db_service.get_contact_information(),
        flat=flat,
    )


@admin.route("/admin/flat/<string:flat_id>/delete", methods=["GET"])
def delete_flat(flat_id: str):
    db_service.delete_flat(flat_id)
    return redirect(url_for("admin.flat_overview"))


@admin.route("/admin/houses", methods=["GET"])
def house_overview():
    houses = db_service.get_all_houses()
    return render_template(
        "admin/house_overview.html",
        rental_objects=get_rental_objects(),
        base_data=db_service.get_contact_information(),
        houses=houses,
    )


@admin.route("/admin/houses/add", methods=["GET", "POST"])
@admin.route("/admin/house/<string:house_id>/update", methods=["GET", "POST"])
def house_form(house_id: str | None = None):
    form = HouseForm()
    house = db_service.get_house_by_id(house_id) if house_id is not None else None
    if request.method == "POST" and form.validate_on_submit():
        data = {
            "name": request.form.get("name"),
            "description": request.form.get("description"),
            "address": request.form.get("address"),
        }
        if house:
            house = db_service.update_house(house.id, **data)
        else:
            house = db_service.create_house(**data)

        return redirect(url_for("admin.house_overview"))

    if house:
        data = {
            "name": house.name,
            "description": house.description,
            "address": house.address,
        }
        form.process(data=data)

    return render_template(
        "admin/house_form.html",
        form=form,
        rental_objects=get_rental_objects(),
        base_data=db_service.get_contact_information(),
        house=house,
    )


@admin.route("/admin/house/<string:house_id>/delete", methods=["GET"])
def delete_house(house_id: str):
    db_service.delete_house(house_id)
    return redirect(url_for("admin.house_overview"))


@admin.route("/admin/<string:object_type>/<string:obj_id>/images", methods=["GET"])
def image_overview(object_type: str, obj_id: str):
    if object_type == "flats":
        obj = db_service.get_flat_by_id(obj_id)
    elif object_type == "houses":
        obj = db_service.get_house_by_id(obj_id)
    else:
        raise ValueError(f"Unknown object type {object_type}")

    assert obj is not None, f"Could not find {object_type} with id {obj_id}. "

    images = obj.images
    return render_template(
        "admin/image_overview.html",
        rental_objects=get_rental_objects(),
        base_data=db_service.get_contact_information(),
        images=images,
        obj=obj,
    )


@admin.route("/admin/<string:object_type>/<string:obj_id>/images/add", methods=["GET", "POST"])
def add_image(object_type: str, obj_id: str):
    form = NewImageForm()
    if request.method == "POST" and form.validate_on_submit():
        file = form.image_file.data

        img_id =str(uuid.uuid4())
        image_dir = Path(app.config["STORAGE_PATH"], "images")
        sub_dir = Path(object_type )/ obj_id
        filename = f"{img_id}.webp"

        with TemporaryDirectory() as temp_dir:
            file.save(Path(temp_dir) / file.filename)

            img = Image.open(Path(temp_dir) / file.filename)
            img.convert("RGB")

            (image_dir / sub_dir).mkdir(exist_ok=True, parents=True)
            img.save(image_dir / sub_dir / filename, "webp")
        
        if object_type == "houses":
            db_service.create_house_image(
                id=img_id,
                title=form.title.data,
                description=form.description.data,
                house_id=obj_id,
            )
        elif object_type == "flats":
            db_service.create_flat_image(
                id=img_id,
                title=form.title.data,
                description=form.description.data,
                flat_id=obj_id,
            )
        else:
            raise ValueError(f"Unknown object type {object_type}")
        
        return redirect(
            url_for("admin.image_overview", object_type=object_type, obj_id=obj_id)
        )

    return render_template(
        "admin/image_form_add.html",
        form=form,
        rental_objects=get_rental_objects(),
        base_data=db_service.get_contact_information(),
    )


@admin.route(
    "/admin/<object_type>/<string:obj_id>/image/<string:img_id>/update",
    methods=["GET", "POST"],
)
def update_image(object_type: Literal["house", "flat"], obj_id: str, img_id: str):
    form = UpdateImageForm()

    if object_type == "flats":
        image = db_service.get_flat_image_by_id(img_id)
    elif object_type == "houses":
        image = db_service.get_house_image_by_id(img_id)
    else:
        raise ValueError(f"Unknown object type {object_type}")


    if request.method == "POST" and form.validate_on_submit():
        if object_type == "house":
            db_service.update_house_image(
                image_id=img_id,
                title=form.title.data,
                description=form.description.data,
            )
        else:
            db_service.update_flat_image(
                image_id=img_id,
                title=form.title.data,
                description=form.description.data,
            )

        return redirect(
            url_for("admin.image_overview", object_type=object_type, obj_id=obj_id)
        )

    data = {"title": image.title, "description": image.description}
    form.process(data=data)
    return render_template(
        "admin/image_form_update.html",
        form=form,
        rental_objects=get_rental_objects(),
        base_data=db_service.get_contact_information(),
        image=image,
    )


@admin.route(
    "/admin/<object_type>/<string:obj_id>/image/<string:img_id>/delete",
    methods=["GET", "POST"],
)
@admin.route("/admin/house/<string:house_id>/delete", methods=["GET"])
def delete_image(object_type: Literal["house", "flat"], obj_id: str, img_id: str):

    if object_type == "flats":
        db_service.delete_flat_image(img_id)
    elif object_type == "houses":
        db_service.delete_house_image(img_id)
    else:
        raise ValueError(f"Unknown object type {object_type}")

    image_dir = Path(app.config["STORAGE_PATH"], "images")
    sub_dir = Path(object_type)/ obj_id
    filename = f"{img_id}.webp"

    (image_dir / sub_dir / filename).unlink()

    return redirect(
        url_for("admin.image_overview", object_type=object_type, obj_id=obj_id)
    )
