from .models import *




def add_flat(name, description, properties) -> Flat:

    flat = Flat.query.filter_by(name=name).first()
    if flat:
        return None
    
    new_flat = Flat(name=name, description=description, properties=properties)
    db.session.add(new_flat)
    db.session.commit()

    return new_flat

def add_flat_image(filename, title, description, type, flatname) -> FlatImage:

    flat_img = FlatImage.query.filter_by(filename=filename).first()
    if flat_img:
        return None
    
    flat = Flat.query.filter_by(name=flatname).first()
    if not flat:
        return None
    
    new_flat_img = FlatImage(filename=filename, title=title, description=description, type=type, flat_id=flat.id)
    db.session.add(new_flat_img)
    db.session.commit()

    return new_flat_img