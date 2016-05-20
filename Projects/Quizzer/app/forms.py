from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField, FieldList, FormField
from wtforms.validators import Length, DataRequired
from app.models import User

class NewTopicForm(Form):
    topic = StringField('Topic', validators=[DataRequired(), Length(min=0, max=255)])

class AnswerForm(Form):
    answer = StringField('Answer', validators=[Length(min=0, max=255)])
    is_correct = BooleanField('IsValidAnswer')

class NewQuestionForm(Form):
    question = StringField('Text', validators=[DataRequired(), Length(min=0, max=255)])
    answers = FieldList(FormField(AnswerForm), min_entries=2)
