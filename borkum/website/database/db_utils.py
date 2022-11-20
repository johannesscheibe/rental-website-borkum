

def cast_to_model(obj, Model):

    if type(obj) == Model:
        return obj

    if type(obj) == str:
        
        return Model.query.filter_by(name=obj).first()

    if type(obj) == int:
        return Model.query.filter_by(id=obj).first()

    raise Exception
    