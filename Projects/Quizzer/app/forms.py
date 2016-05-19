from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, FieldList
from wtforms.validators import Length, DataRequired
from app.models import User

class NewTopicForm(Form):
    topic = StringField('Topic', validators=[DataRequired(), Length(min=0, max=255)])

class NewQuestionForm(Form):
    question = StringField('Text', validators=[DataRequired(), Length(min=0, max=255)])
    answers = FieldList(StringField('Answer', validators=[Length(min=0, max=255)]), min_entries=1)
    validities = FieldList(BooleanField('IsValidAnswer'), min_entries=1)
