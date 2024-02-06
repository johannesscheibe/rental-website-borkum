from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (
    RadioField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
    widgets,
)
from wtforms.validators import InputRequired


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """

    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class FlatForm(FlaskForm):
    name = StringField("Wohnungsname", validators=[InputRequired()])
    description = TextAreaField("Beschreibung")
    house = RadioField("Haus", choices=[], validators=[InputRequired()])

    tags = MultiCheckboxField("Tags", choices=[])

    submit = SubmitField("Speichern")


class HouseForm(FlaskForm):
    name = StringField("Hausname", validators=[InputRequired()])
    description = TextAreaField("Beschreibung")
    address = StringField("Adresse", validators=[InputRequired()])

    submit = SubmitField("Speichern")


class NewImageForm(FlaskForm):
    image_file = FileField(
        "Bild",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "jpeg", "png"], "Images only!"),
        ],
    )
    title = StringField("Titel", validators=[InputRequired()])
    description = StringField("Beschreibung", validators=[InputRequired()])

    submit = SubmitField("Speichern")


class UpdateImageForm(FlaskForm):
    title = StringField("Titel", validators=[InputRequired()])
    description = StringField("Beschreibung", validators=[InputRequired()])

    submit = SubmitField("Speichern")
