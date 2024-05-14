from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    file = FileField('Resume File', validators=[DataRequired()])
    label = IntegerField('Label (0 or 1)', validators=[DataRequired()])
    submit = SubmitField('Submit')
