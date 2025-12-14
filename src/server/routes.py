from flask import render_template, request, jsonify, redirect, url_for, session
from server import app, db
from server.forms import MainButtonsForm, LoginForm, RegistrationForm, ProfileUsernameForm, ProfilePasswordForm
from server.user import User
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash
from server.custom_paginated import CustomPaginated

@app.route('/')
@login_required
def index():
    form = MainButtonsForm()
    # TEST the interface with dummy data
    # if 'paginated' not in session or session['paginated'] is None:
    #     session['paginated'] = CustomPaginated(['A', 'B'], [['a1','b1'], ['a2','b2'], ['a3','b3']], 2).to_dict()
    #     session['hints'] = ['Hint A', 'Hint B', 'Hint C']
    paginated = CustomPaginated.from_dict(session['paginated'])
    hints = session['hints'] if 'hints' in session else None
    print(session['paginated'])
    return render_template('index.html', form=form, paginated=paginated, is_admin=current_user.is_admin, hints=hints)


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

from dialogues.dialogue_logic import DialogueProcessor
dummy_dialogue_processor = DialogueProcessor(db) #TODO replace with dialogue processor of user

#TODO require login
#@login_required
@app.route('/agent', methods=['POST'])
def agent():
    if request.is_json:
        data = request.get_json()
        text = data.get('text')
        if text:
            result = dummy_dialogue_processor.process_user_text(text)
            result_paginated = CustomPaginated(result['table_header'], result['table_body'], 10) if 'table_header' in result and 'table_body' in result and result['table_body'] is not None else None
            result_hints = result['hints'] if 'hints' in result else None
            session['hints'] = result_hints
            session['paginated'] = result_paginated.to_dict() if result_paginated else None
            return jsonify({'text':result['text'], 'emotion':result['emotion'], 'table':render_template('table.html', paginated=result_paginated), 'hints':render_template('list.html', hints=result_hints)}), 200
        else:
            return jsonify({'status':'error', 'message':'Expected "text" key in JSON'}), 400
    else:
        return jsonify({'status':'error', 'message':'Expected JSON'}), 400

@login_required
@app.route('/make_faw/<int:book_id>', methods=['POST'])
def make_faw(book_id: int):
    # TODO call db with current user id and passed book id to make the book faw
    return jsonify({'status': 'ok'}), 200

@login_required
@app.route('/paginated/next', methods=['GET', 'POST'])
def paginated_next():
    paginated = CustomPaginated.from_dict(session['paginated'])
    paginated.set_page(paginated.next_page_num())
    session['paginated'] = paginated.to_dict()
    return render_template('table.html', paginated=paginated)

@login_required
@app.route('/paginated/prev', methods=['GET', 'POST'])
def paginated_prev():
    paginated = CustomPaginated.from_dict(session['paginated'])
    paginated.set_page(paginated.prev_page_num())
    session['paginated'] = paginated.to_dict()
    return render_template('table.html', paginated=paginated)


from server import routes_admin
