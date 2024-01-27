from typing import Type


def cast_to_model(obj, Model):
    from borkum.website.database.models import Image

    if type(obj) == Model:
        return obj

    if type(obj) == str:
        if Model == Image:
            return Model.query.filter_by(filepath=obj).first()
        return Model.query.filter_by(name=obj).first()

    if type(obj) == int:
        return Model.query.filter_by(id=obj).first()

    raise Exception
