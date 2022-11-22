import json
import os

from borkum.website.database import db_service
from borkum.website.database.models import Apartment, House, Image, Tag
from flask import Blueprint
from flask import current_app as app
from flask import redirect, render_template, request, url_for

from .utils.forms import ApartmentForm, HouseForm

admin = Blueprint("admin", __name__)


@admin.route("/admin", methods=["GET", "POST"])
# @login_required
def admin_page():
    return render_template("admin/index.html", base_data=app.config["BASE_DATA"])


@admin.route("/admin/apartments", methods=["GET", "POST"])
# @login_required
def apartment_overview():
    apartments = Apartment.filter()
    return render_template(
        "admin/apartment_overview.html",
        base_data=app.config["BASE_DATA"],
        apartments=apartments,
    )


@admin.route("/admin/apartments/form", methods=["GET", "POST"], defaults={"name": None})
@admin.route("/admin/apartments/form/<string:name>", methods=["GET", "POST"])
# @login_required
def apartment_form(name=None):

    apartment = Apartment.filter(name=name).first()
    if request.method == "POST":
        data = {
            "displayname": request.form.get("displayname"),
            "description": request.form.get("description"),
            "house": int(request.form.get("house"))
            if request.form.get("house")
            else None,
            "tags": list(map(int, request.form.getlist("tags"))),
            "thumbnail": int(request.form.get("thumbnail"))
            if request.form.get("thumbnail")
            else None,
        }
        if apartment:
            apartment = db_service.update_apartment(apartment.id, **data)
        else:
            apartment = db_service.add_apartment(**data)

        if apartment:
            return redirect(
                url_for("admin.apartment_overview", base_data=app.config["BASE_DATA"])
            )

    form = ApartmentForm()
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.filter()]
    form.house.choices = [(house.id, house.displayname) for house in House.filter()]
    form.thumbnail.choices = (
        [(img.id, img.filepath) for img in apartment.images] if apartment.images else []
    )
    if apartment:
        data = {
            "displayname": apartment.displayname,
            "description": apartment.description,
            "house": apartment.house.id if apartment.house else None,
            "tags": [tag.id for tag in apartment.tags],
            "thumbnail": apartment.thumbnail.id if apartment.thumbnail else None,
        }
        form.process(data=data)

    return render_template(
        "admin/apartment_form.html", form=form, base_data=app.config["BASE_DATA"]
    )


@admin.route("/admin/houses", methods=["GET", "POST"])
# @login_required
def house_overview():
    houses = House.filter()
    return render_template(
        "admin/house_overview.html", base_data=app.config["BASE_DATA"], houses=houses
    )


@admin.route("/admin/houses/form", methods=["GET", "POST"], defaults={"name": None})
@admin.route("/admin/houses/form/<string:name>", methods=["GET", "POST"])
# @login_required
def house_form(name=None):

    house = House.filter(name=name).first()
    if request.method == "POST":
        data = {
            "displayname": request.form.get("displayname"),
            "description": request.form.get("description"),
            "address": request.form.get("address"),
            "thumbnail": int(request.form.get("thumbnail"))
            if request.form.get("thumbnail")
            else None,
        }
        if house:
            house = db_service.update_house(house.id, **data)
        else:
            house = db_service.add_house(**data)

        if house:
            return redirect(
                url_for("admin.house_overview", base_data=app.config["BASE_DATA"])
            )

    form = HouseForm()
    form.thumbnail.choices = (
        [(img.id, img.filepath) for img in house.images] if house.images else []
    )
    if house:
        data = {
            "displayname": house.displayname,
            "description": house.description,
            "address": house.address,
            "thumbnail": house.thumbnail.id if house.thumbnail else None,
        }
        form.process(data=data)

    return render_template(
        "admin/house_form.html", form=form, base_data=app.config["BASE_DATA"]
    )
