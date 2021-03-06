from flask import render_template,g
from app import app, db, lm
from flask.ext.login import login_user, logout_user, current_user, login_required, redirect, url_for, flash, request
from auth import OAuthSignIn
from models import User, Topic, Question, Answer, Attempt
from forms import NewTopicForm, NewQuestionForm, AnswerForm

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html',
                           title='Home')


@app.route('/topics', methods=['GET', 'POST'])
@app.route('/topics/<operation>/<int:topic_id>', methods=['GET', 'POST'])
def topics(operation=None, topic_id=-1):
    form = NewTopicForm(request.form)
    
    if request.method == 'POST' and form.validate_on_submit():
        topic = Topic(name=form.topic.data)
        db.session.add(topic)
        db.session.commit()
        flash('New topic is created')
        return redirect(url_for('topics'))
    if operation == 'delete':
        try:
            topic = Topic().query.get(topic_id)
            db.session.delete(topic)
            db.session.commit()
        except:
            flash ("Failed to delete topic {}.".format(topic_id))
        return redirect(url_for('topics'))
    if operation == 'update':
        try:
            topic = Topic().query.get(topic_id)
            topic.name = request.values.get("value")
            db.session.add(topic)
            db.session.commit()
        except:
            return 'Error renaming topic.', 400
        else:
            return 'Topic updted successfuly.', 200

    topics = Topic().query.all()  
    return render_template('topics.html',
                           title='Topics',
                           form = form,
                           topics = topics)

@app.route('/topic/questions/<topic_id>', methods=['GET', 'POST'])
def topic_questions(topic_id = None):
    if topic_id == None:
        return "Topic id not found", 404
    topic = Topic().query.get(topic_id)
    
    return render_template('topic_questions.html',
                           title='Questions for topic {}'.format(topic.name),
                           topic_id = topic_id,
                           questions = topic.questions)


@app.route('/question/new/<int:topic_id>', methods=['GET', 'POST'])
def new_question(topic_id=-1):
    form = NewQuestionForm(request.form)
    #answerzip = zip(form.answers, form.validities)
    answers = []
    if request.method == 'POST' and form.validate_on_submit():
        for answer in form.answers:
            answers.append(Answer(text=answer.answer.data, is_correct=answer.is_correct.data))
            
        question = Question(text=form.question.data,author=g.user,topic=Topic.query.get(topic_id), answers=answers)
        db.session.add(question)
        db.session.commit()
        
        return redirect(url_for('topic_questions', topic_id=topic_id))
        #question = Question(texty, author, topic, answers)
        
    return render_template('question.html',
                           title='New Question',
                           form = form)
    
@app.route('/question/delete/<int:question_id>', methods=['GET'])
def delete_question(question_id=-1):
    question = Question.query.get(question_id)
    topic_id = question.topic.id

    db.session.delete(question)
    db.session.commit()
        
    return redirect(url_for('topic_questions', topic_id=topic_id))

@app.route('/question/edit/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id=-1):
    form = NewQuestionForm(request.form)
    #answerzip = zip(form.answers, form.validities)
    answers = []
    if request.method == 'POST' and form.validate_on_submit():
        for answer in form.answers:
            answers.append(Answer(text=answer.answer.data, is_correct=answer.is_correct.data))
        
        question = Question.query.get(question_id)
        question.text = form.question.data
        Answer.query.filter(Answer.question_id==question.id).delete()
        question.answers = answers
        db.session.add(question)
        db.session.commit()
        
        return redirect(url_for('topic_questions', topic_id = question.topic.id))

    question = Question.query.get(question_id)
    for i in range(2):
        form.answers.pop_entry()

    form.question.data = question.text
    for answer in question.answers:
        answer_form = AnswerForm()
        answer_form.answer = answer.text
        answer_form.is_correct = answer.is_correct
        form.answers.append_entry(answer_form)
        
    return render_template('question.html',
                           title='New Question',
                           form = form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html', 
                           title='Sign In')

from flask.ext.login import login_user, logout_user, current_user, login_required

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    # Flask-Login function
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    username, email = oauth.callback()
    if email is None:
        # I need a valid email address for my user identification
        flash('Authentication failed.')
        return redirect(url_for('index'))
    # Look if the user already exists
    user=User.query.filter_by(email=email).first()
    if not user:
        # Create the user. Try and use their name returned by Google,
        # but if it is not set, split the email address at the @.
        nickname = username
        if nickname is None or nickname == "":
            nickname = email.split('@')[0]

        # We can do more work here to ensure a unique nickname, if you 
        # require that.
        user=User(nickname=nickname, email=email)
        db.session.add(user)
        db.session.commit()
    # Log in the user, by default remembering them for their next visit
    # unless they log out.
    login_user(user, remember=True)
    return redirect(url_for('index'))