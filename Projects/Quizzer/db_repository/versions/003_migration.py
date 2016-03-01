from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
answer = Table('answer', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String(length=255)),
    Column('is_correct', Boolean),
    Column('question_id', Integer),
)

attempt = Table('attempt', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('score', Float(precision=2)),
    Column('student_name', String(length=255)),
    Column('student_email', String(length=255)),
    Column('timestamp', DateTime),
)

question = Table('question', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String(length=255)),
    Column('topic_id', Integer),
    Column('author_id', Integer),
)

result_answers = Table('result_answers', post_meta,
    Column('attempt_id', Integer),
    Column('answer_id', Integer),
)

topic = Table('topic', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=255)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nickname', String(length=64)),
    Column('email', String(length=120)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['answer'].create()
    post_meta.tables['attempt'].create()
    post_meta.tables['question'].create()
    post_meta.tables['result_answers'].create()
    post_meta.tables['topic'].create()
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['answer'].drop()
    post_meta.tables['attempt'].drop()
    post_meta.tables['question'].drop()
    post_meta.tables['result_answers'].drop()
    post_meta.tables['topic'].drop()
    post_meta.tables['user'].drop()
