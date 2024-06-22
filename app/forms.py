from flask_wtf import FlaskForm
from wtforms import FileField, SelectField, SubmitField
from wtforms.validators import InputRequired


class TrainForm(FlaskForm):
    file = FileField('Resume File', validators=[InputRequired()])
    label = SelectField('Label', choices=[('0', '0'), ('1', '1')], validators=[InputRequired()])
    submit = SubmitField('Submit')


class PredictForm(FlaskForm):
    file = FileField('Resume File', validators=[InputRequired()])
    submit = SubmitField('Submit')
