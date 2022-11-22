from flask_wtf import FlaskForm
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


class ApartmentForm(FlaskForm):

    displayname = StringField("Wohnungsname", validators=[InputRequired()])
    description = TextAreaField("Beschreibung")
    house = RadioField("Haus", choices=[], validators=[InputRequired()])
    thumbnail = RadioField("Thumbnail", choices=[])

    tags = MultiCheckboxField("Tags", choices=[])

    submit = SubmitField("Speichern")


class HouseForm(FlaskForm):

    displayname = StringField("Hausname", validators=[InputRequired()])
    description = TextAreaField("Beschreibung")
    address = StringField("Adresse", validators=[InputRequired()])
    thumbnail = RadioField("Thumbnail", choices=[])

    submit = SubmitField("Speichern")
