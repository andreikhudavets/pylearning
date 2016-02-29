from flask import render_template,g
from app import app, db
from flask.ext.login import login_user, logout_user, current_user, login_required

@app.before_request
def before_request():
    g.user = current_user
        
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html',
                           title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('login.html', 
                           title='Sign In')
