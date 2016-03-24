from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import Length, DataRequired
from app.models import User

class NewTopicForm(Form):
    topic = StringField('Topic', validators=[DataRequired(), Length(min=0, max=255)])
