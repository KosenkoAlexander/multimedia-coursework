from flask import render_template, request, jsonify, redirect, url_for
from server import app
from server.forms import MainButtonsForm, LoginForm, RegistrationForm
from server.user import User
from flask_login import current_user, login_user, login_required
from werkzeug.security import generate_password_hash

@app.route('/')
@login_required
def index():
    form = MainButtonsForm()
    return render_template('index.html', form=form)


@app.route('/start', methods=['POST'])
def start():
    data = request.form
    if data:
        return jsonify(status = 'success'), 200
    else:
        return jsonify(status = 'error', message = 'no data'), 400


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User(0, 'test_username', 'test_email', generate_password_hash('pass')) #TODO replace with call to DB
        if user is None or not user.check_password(form.password.data):
            #TODO add response
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password_hash=generate_password_hash(form.password.data))
        return redirect(url_for('login'))
    return render_template('register.html', form=form)
