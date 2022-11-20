from flask import Blueprint, render_template, current_app as app
import os

legal_information = Blueprint('legal_information', __name__)

@legal_information.route('/impressum')
def impressum():
    return render_template("impressum.html",  base_data=app.config['BASE_DATA'])


@legal_information.route('/privacy')
def privacy():
    return render_template("privacy.html",  base_data=app.config['BASE_DATA'])


@legal_information.route('/terms_of_use')
def terms_of_use():
    return render_template("terms_of_use.html",  base_data=app.config['BASE_DATA'])

