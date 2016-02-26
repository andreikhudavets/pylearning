import os
from config import basedir
from app import app, db
from app.models import User, Question, Topic

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
    
    def test_questions(self):
        topic = Topic(name="test topic")
        user = User(nickname="andrei", email="test@test.com")
        question_1 = Question(text="test question #1", topic=topic, author=user)
        question_2 = Question(text="test question #2", topic=topic, author=user)
        db.session.add(user)
        db.session.add(question_1)
        db.session.add(question_2)
        db.session.commit()
        user = User.query.first()
        assert len(user.questions) == 2
        
        
        