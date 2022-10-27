import json
import os

from borkum.website.database import db_service
from borkum.website.database.models import House
from flask import Blueprint
from flask import current_app as app
from flask import redirect, render_template, request, url_for

from .utils.forms import ApartmentForm

admin = Blueprint('admin', __name__)


@admin.route('/admin', methods=['GET', 'POST'])
#@login_required
def admin_page(id=None):
    return render_template(
        "admin/index.html",
        contact=app.config['CONTACT']
    )

@admin.route('/admin/apartments', methods=['GET', 'POST'])
#@login_required
def apartment_page():
    return render_template(
        "admin/apartments.html",
        contact=app.config['CONTACT']
    )

@admin.route('/admin/apartments/form', methods=['GET', 'POST'], defaults={'id': None})
@admin.route('/admin/apartments/form/<string:id>', methods=['GET', 'POST'])
#@login_required
def apartment_form(id=None):
    form = ApartmentForm()
    form.tags.choices = ["1", "2", "3"]
    form.thumbnail.choices = ["img1", "img2", "img3"]
    form.images.choices = ["img1", "img2", "img3"]

    if request.method == 'POST':
        data = {
            "name" : request.form.get('name'),
            "description" : request.form.get('description'),
            "house" : None,
            "tags" : [],
            "thumbnail": None,
            "images" : [],
        }
        # if id:
        #     apartment = db_service.update_apartment(id=id, **data)
        # else:
        
        apartment = db_service.add_apartment(**data)
            
        if apartment:  
            return redirect(url_for('admin.admin_page', contact=app.config['CONTACT'])) 
    
        
    if id:
        # load apartment
        pass
    
    
    return render_template(
        "admin/apartment_form.html",
        data=None,
        form=form,
        contact=app.config['CONTACT']
    )


