from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class DbForm(FlaskForm):
    db_name = StringField(label='Database name')
    submit = SubmitField(label='Submit')
