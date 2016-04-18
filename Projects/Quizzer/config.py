# -*- coding: utf-8 -*-

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

CSRF_ENABLED = True
SECRET_KEY = '437HJKlkjH^&*967'

GOOGLE_LOGIN_CLIENT_ID = "176466295225-ree0l8grtmnri3452kr5arj0rleqk78t.apps.googleusercontent.com"
GOOGLE_LOGIN_CLIENT_SECRET = "2uoyVX-NnEKbqISbTZJQQyah"

OAUTH_CREDENTIALS={
        'google': {
            'id': GOOGLE_LOGIN_CLIENT_ID,
            'secret': GOOGLE_LOGIN_CLIENT_SECRET
        }
}