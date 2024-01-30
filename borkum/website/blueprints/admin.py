import os
from pathlib import Path
from typing import Literal
import uuid

from flask import Blueprint
from flask import current_app as app
from flask import redirect, render_template, request, url_for
from loguru import logger
from werkzeug.utils import secure_filename

from borkum.website.database import db_service

from .utils.forms import FlatForm, HouseForm, ImageForm

admin = Blueprint("admin", __name__)


@admin.route("/admin", methods=["GET", "POST"])
# @login_required
def admin_page():
    return render_template("admin/index.html", base_data=app.config["BASE_DATA"])


@admin.route("/admin/flats", methods=["GET", "POST"])
# @login_required
def flat_overview():
    flats = db_service.get_all_flats()
    return render_template(
        "admin/flat_overview.html",
        base_data=app.config["BASE_DATA"],
        flats=flats,
    )


@admin.route("/admin/flats/add", methods=["GET", "POST"], defaults={"id": None})
@admin.route("/admin/flats/<int:id>/update", methods=["GET", "POST"])
# @login_required
def flat_form(id=None):
    flat = db_service.get_flat_by_id(id) if id is not None else None

    if request.method == "POST":
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

        if flat:
            return redirect(
                url_for("admin.flat_overview", base_data=app.config["BASE_DATA"])
            )

    form = FlatForm()
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
        "admin/flat_form.html", form=form, base_data=app.config["BASE_DATA"]
    )


@admin.route("/admin/flats/<int:id>/delete", methods=["GET"])
# @login_required
def delete_flat(id: int):
    db_service.delete_flat(id)
    return redirect(url_for("admin.flat_overview", base_data=app.config["BASE_DATA"]))


@admin.route("/admin/houses", methods=["GET", "POST"])
# @login_required
def house_overview():
    houses = db_service.get_all_houses()
    return render_template(
        "admin/house_overview.html", base_data=app.config["BASE_DATA"], houses=houses
    )


@admin.route("/admin/houses/add", methods=["GET", "POST"], defaults={"id": None})
@admin.route("/admin/houses/<int:id>/update", methods=["GET", "POST"])
# @login_required
def house_form(id=None):
    house = db_service.get_house_by_id(id) if id is not None else None
    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "description": request.form.get("description"),
            "address": request.form.get("address"),
        }
        if house:
            house = db_service.update_house(house.id, **data)
        else:
            house = db_service.create_house(**data)

        if house:
            return redirect(
                url_for("admin.house_overview", base_data=app.config["BASE_DATA"])
            )

    form = HouseForm()
    if house:
        data = {
            "name": house.name,
            "description": house.description,
            "address": house.address,
        }
        form.process(data=data)

    return render_template(
        "admin/house_form.html", form=form, base_data=app.config["BASE_DATA"]
    )


@admin.route("/admin/houses/<int:id>/delete", methods=["GET"])
# @login_required
def delete_house(id: int):
    db_service.delete_house(id)
    return redirect(url_for("admin.house_overview", base_data=app.config["BASE_DATA"]))


@admin.route(
    "/admin/houses/<int:id>/add-image",
    methods=["GET", "POST"],
    defaults={"object_type": "house"},
)
@admin.route(
    "/admin/flats/<int:id>/add-image",
    methods=["GET", "POST"],
    defaults={"object_type": "flat"},
)
# @login_required
def add_image(id: int, object_type: Literal["house", "flat"]):
    form = ImageForm()
    if form.validate_on_submit():
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
                house_id=id,
            )
            return redirect(
                url_for("admin.admin_page", base_data=app.config["BASE_DATA"])
            )
        elif object_type == "flat":
            db_service.create_flat_image(
                image_url=str(sub_dir / filename),
                title=form.title.data,
                description=form.description.data,
                flat_id=id,
            )
            return redirect(
                url_for("admin.admin_page", base_data=app.config["BASE_DATA"])
            )
        else:
            logger.warning(
                f"Tried to add image for an unknown object type {object_type}"
            )

    return render_template(
        "admin/image_form.html",
        form=form,
        base_data=app.config["BASE_DATA"],
    )
