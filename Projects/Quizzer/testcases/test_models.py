import os
from config import basedir
from app import app, db
from app.models import User, Question, Topic, Answer, Attempt
from datetime import datetime
import unittest

class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_basic_flow(self):
        topic = Topic(name="test topic")
        user = User(nickname="andrei", email="test@test.com")
        answers_1 = [Answer(text="Answer #1", is_correct=True), Answer(text="Answer #2", is_correct=False)]
        answers_2 = [Answer(text="Answer #3", is_correct=True), Answer(text="Answer #4", is_correct=False)]
        question_1 = Question(text="test question #1", topic=topic, author=user, answers=answers_1)
        question_2 = Question(text="test question #2", topic=topic, author=user, answers=answers_2)
        db.session.add(question_1)
        db.session.add(question_2)
        db.session.commit()
        user = User.query.first()
        
        #Checking question references
        assert Question.query.get(1).author.nickname == "andrei"
        assert Question.query.get(1).answers[0].text == "Answer #1"
        assert Question.query.get(1).topic.name == "test topic"
        
        #Checking topic references
        assert len(Topic.query.get(1).questions) == 2

        #Checking user references        
        assert len(User.query.get(1).questions) == 2
        
        attempt = Attempt(timestamp = datetime.utcnow(), student_name="stefan", student_email="stefan@test.com", score=99.5)
        attempt.answers.append(Question.query.get(1).answers[0])
        attempt.answers.append(Question.query.get(2).answers[1])
        db.session.add(attempt)
        db.session.commit()

        #Checking answer refferences
        assert Answer.query.filter(Answer.text=="Answer #1").first().attempts[0].student_name == "stefan"
        assert Answer.query.filter(Answer.text=="Answer #1").first().question.text == "test question #1"
        
        #Checking attempt refferences
        assert len(Attempt.query.get(1).answers) == 2
        
        
        