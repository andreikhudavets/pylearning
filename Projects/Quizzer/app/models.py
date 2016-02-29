from app import db, app
ROLE_GUEST = 0
ROLE_USER = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    questions = db.relationship("Question", back_populates="author")
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3
    
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    questions = db.relationship("Question", back_populates="topic")
    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship("User", back_populates="questions")
    topic = db.relationship("Topic", back_populates="questions")
    answers = db.relationship("Answer", back_populates="question")
    
result_answers = db.Table('result_answers', db.Model.metadata,
    db.Column('attempt_id', db.Integer, db.ForeignKey('attempt.id')),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id'))
)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    is_correct = db.Column(db.Boolean())
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship("Question", back_populates="answers")
    attempts = db.relationship("Attempt", secondary=result_answers, back_populates='answers')

class Attempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float(precision=2))
    student_name = db.Column(db.String(255))
    student_email = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime)
    answers = db.relationship("Answer", secondary=result_answers, back_populates='attempts')
    