from flask import flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask_login import current_user
from travelly.models import Location
from travelly.locations.utils import remove_accents, get_lat_lng

class AddLocationForm(FlaskForm):
    street = StringField('Street', validators=[DataRequired()],
                        render_kw={"placeholder": "Street"})
    number = StringField('Number', validators=[DataRequired()],
                        render_kw={"placeholder": "Number"}) #string, because numbers can be with letters ex. '48A'
    code = StringField('Code', validators=[DataRequired()],
                        render_kw={"placeholder": "City Code"})
    city = StringField('City', validators=[DataRequired()],
                        render_kw={"placeholder": "City"})

    submit = SubmitField('Add Location')

class UpdateLocationForm(FlaskForm):
    street = StringField('Street', validators=[DataRequired()],
                        render_kw={"placeholder": "Street"})
    number = StringField('Number', validators=[DataRequired()],
                        render_kw={"placeholder": "Number"}) #sting, because numbers can be with letters ex. '48A'
    code = StringField('Code', validators=[DataRequired()],
                        render_kw={"placeholder": "City Code"})
    city = StringField('City', validators=[DataRequired()],
                        render_kw={"placeholder": "City"})

    submit = SubmitField('Update')

# class MultiCheckboxField(SelectMultipleField):
#     widget = widgets.ListWidget(prefix_label=False)
#     option_widget = widgets.CheckboxInput()

# class DeleteForm(FlaskForm):
#     choices = MultiCheckboxField('Routes', coerce=int)
#     submit = SubmitField("Set User Choices")

class CSVForm(FlaskForm):
    csv = FileField('Upload CSV', validators=[FileAllowed(['csv'])])
    submit = SubmitField('Upload')