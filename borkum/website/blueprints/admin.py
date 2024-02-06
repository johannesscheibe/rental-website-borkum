import os
from pathlib import Path
from typing import Literal
import uuid

from flask import (
    Blueprint,
    current_app as app,
    redirect,
    render_template,
    request,
    url_for,
)
from loguru import logger
from werkzeug.utils import secure_filename

from borkum.website.database import db_service

from .utils.forms import FlatForm, HouseForm, NewImageForm, UpdateImageForm

admin = Blueprint("admin", __name__)


def get_base_data():
    return app.config["BASE_DATA"]


@admin.route("/admin", methods=["GET"])
def admin_page():
    return render_template("admin/index.html", base_data=get_base_data())


@admin.route("/admin/flats", methods=["GET"])
def flat_overview():
    flats = db_service.get_all_flats()
    return render_template(
        "admin/flat_overview.html",
        base_data=get_base_data(),
        flats=flats,
    )


@admin.route("/admin/flats/add", methods=["GET", "POST"])
@admin.route("/admin/flat/<int:flat_id>/update", methods=["GET", "POST"])
def flat_form(flat_id: int | None = None):
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
        "admin/flat_form.html", form=form, base_data=get_base_data(), flat=flat
    )


@admin.route("/admin/flat/<int:flat_id>/delete", methods=["GET"])
def delete_flat(flat_id: int):
    db_service.delete_flat(flat_id)
    return redirect(url_for("admin.flat_overview"))


@admin.route("/admin/houses", methods=["GET"])
def house_overview():
    houses = db_service.get_all_houses()
    return render_template(
        "admin/house_overview.html", base_data=get_base_data(), houses=houses
    )


@admin.route("/admin/houses/add", methods=["GET", "POST"])
@admin.route("/admin/house/<int:house_id>/update", methods=["GET", "POST"])
def house_form(house_id: int | None = None):
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
        "admin/house_form.html", form=form, base_data=get_base_data(), house=house
    )


@admin.route("/admin/house/<int:house_id>/delete", methods=["GET"])
def delete_house(house_id: int):
    db_service.delete_house(house_id)
    return redirect(url_for("admin.house_overview"))


@admin.route("/admin/<object_type>/<int:obj_id>/images", methods=["GET"])
def image_overview(object_type: Literal["house", "flat"], obj_id: int):
    obj_getter = getattr(db_service, f"get_{object_type}_by_id")
    obj = obj_getter(obj_id)

    assert obj is not None, f"Could not find {object_type} with id {obj_id}. "

    images = obj.images
    return render_template(
        "admin/image_overview.html",
        base_data=get_base_data(),
        images=images,
        obj=obj,
        object_type=object_type,
    )


@admin.route("/admin/<object_type>/<int:obj_id>/images/add", methods=["GET", "POST"])
def add_image(object_type: Literal["house", "flat"], obj_id: int):
    form = NewImageForm()
    if request.method == "POST" and form.validate_on_submit():
        file = form.image_file.data
        ext = file.filename.split(".")[-1]

        image_dir = Path(app.config["STORAGE_PATH"], "img")
        sub_dir = Path("uploads")
        filename = str(uuid.uuid4()) + "." + ext

        (image_dir / sub_dir).mkdir(exist_ok=True, parents=True)

        file.save(image_dir / sub_dir / filename)

        if object_type == "house":
            db_service.create_house_image(
                image_url=str(sub_dir / filename),
                title=form.title.data,
                description=form.description.data,
                house_id=obj_id,
            )
        else:
            db_service.create_flat_image(
                image_url=str(sub_dir / filename),
                title=form.title.data,
                description=form.description.data,
                flat_id=obj_id,
            )
        return redirect(
            url_for("admin.image_overview", obj_id=obj_id, object_type=object_type)
        )

    return render_template(
        "admin/image_form_add.html", form=form, base_data=get_base_data()
    )


@admin.route(
    "/admin/<object_type>/<int:obj_id>/image/<int:img_id>/update",
    methods=["GET", "POST"],
)
def update_image(object_type: Literal["house", "flat"], obj_id: int, img_id: int):
    form = UpdateImageForm()
    image_getter = getattr(db_service, f"get_{object_type}_image_by_id")
    image = image_getter(img_id)

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
            url_for("admin.image_overview", obj_id=obj_id, object_type=object_type)
        )

    data = {"title": image.title, "description": image.description}
    form.process(data=data)
    return render_template(
        "admin/image_form_update.html",
        form=form,
        base_data=get_base_data(),
        image=image,
    )


@admin.route(
    "/admin/<object_type>/<int:obj_id>/image/<int:img_id>/delete",
    methods=["GET", "POST"],
)
@admin.route("/admin/house/<int:house_id>/delete", methods=["GET"])
def delete_image(object_type: Literal["house", "flat"], obj_id: int, img_id: int):
    image_deleter = getattr(db_service, f"delete_{object_type}_image")
    image_deleter(img_id)

    return redirect(
        url_for("admin.image_overview", obj_id=obj_id, object_type=object_type)
    )
