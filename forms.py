from wtforms.validators import DataRequired, Length, EqualTo
from wtforms import StringField, PasswordField, validators, Form, SubmitField, IntegerField, SelectField



class Track(Form):
    num = IntegerField("Search For Location", validators=[DataRequired()])