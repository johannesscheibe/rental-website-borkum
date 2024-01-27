from pathlib import Path

from flask import Blueprint
from flask import current_app as app
from flask import redirect, render_template, request, url_for
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


@admin.route("/admin/flats/form", methods=["GET", "POST"], defaults={"id": None})
@admin.route("/admin/flats/form/<int:id>", methods=["GET", "POST"])
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


@admin.route("/admin/flats/delete/<int:id>", methods=["GET"])
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


@admin.route("/admin/houses/form", methods=["GET", "POST"], defaults={"id": None})
@admin.route("/admin/houses/form/<int:id>", methods=["GET", "POST"])
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


@admin.route("/admin/house/delete/<int:id>", methods=["GET"])
# @login_required
def delete_house(id: int):
    db_service.delete_house(id)
    return redirect(url_for("admin.house_overview", base_data=app.config["BASE_DATA"]))


@admin.route("/admin/images", methods=["GET", "POST"])
# @login_required
def image_form():
    form = ImageForm()
    if form.validate_on_submit():
        file = form.image_file.data
        filename = secure_filename(file.filename)
        target_path = Path(app.root_path, "static", "img", "uploads")
        target_path.mkdir(exist_ok=True, parents=True)
        file.save(target_path / filename)

        db_service.create_image(
            image_url=str(target_path / filename),
            title=form.title.data,
            description=form.description.data,
        )
        return redirect(url_for("admin.admin_page", base_data=app.config["BASE_DATA"]))
    return render_template(
        "admin/flat_image_form.html",
        form=form,
        base_data=app.config["BASE_DATA"],
    )
