from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange


class TrainForm(FlaskForm):
    file = FileField('Resume File', validators=[InputRequired()])
    label = IntegerField('Label (0 or 1)', validators=[InputRequired(), NumberRange(min=0, max=1)])
    submit = SubmitField('Train')


class PredictForm(FlaskForm):
    file = FileField('Resume File', validators=[InputRequired()])
    submit = SubmitField('Predict')
