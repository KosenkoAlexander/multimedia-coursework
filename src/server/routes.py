from flask import render_template, request, jsonify, redirect, url_for
from server import app
from server.forms import MainButtonsForm, LoginForm, RegistrationForm, ProfileUsernameForm, ProfilePasswordForm
from server.user import User
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash
from server.custom_paginated import CustomPaginated

@app.route('/')
@login_required
def index():
    form = MainButtonsForm()
    if not current_user.paginated:
        current_user.paginated = CustomPaginated(['A', 'B'], [['a1','b1'], ['a2','b2'], ['a3','b3']], 2)
    paginated = current_user.paginated
    if paginated:
        page = request.args.get('page', 0, type=int)
        paginated.set_page(page)
    return render_template('index.html', form=form, paginated=paginated)


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
            return render_template('login.html', form=form, login_error = 'Wrong username or password')#redirect(url_for('login'))
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

@login_required
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form_username = ProfileUsernameForm()
    form_password = ProfilePasswordForm()
    if form_username.validate_on_submit():
        #TODO
        return render_template('profile.html', form_username=form_username, form_password=form_password)
    if form_password.validate_on_submit():
        #TODO
        return render_template('profile.html', form_username=form_username, form_password=form_password)
    return render_template('profile.html', form_username=form_username, form_password=form_password)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
