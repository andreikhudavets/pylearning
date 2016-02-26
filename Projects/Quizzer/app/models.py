from app import db, app
ROLE_GUEST = 0
ROLE_USER = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    questions = db.relationship("Question", back_populates="author")
    
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    questions = db.relationship("Question", back_populates="topic")
    results = db.relationship("Result", back_populates="topic")
    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship("User", back_populates="questions")
    topic = db.relationship("Topic", back_populates="questions")
    
class Variant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    is_correct = db.Column(db.Boolean())
    
class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.relationship("Topic", back_populates="results")
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
    student_name = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime)