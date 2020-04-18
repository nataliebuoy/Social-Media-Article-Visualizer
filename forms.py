from flask_wtf import FlaskForm
from wtforms import StringField

class KeywordForm(FlaskForm):
    kw = StringField('keyword')


