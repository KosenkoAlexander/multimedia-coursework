from flask import render_template, request, jsonify, redirect, url_for, session, flash
from server import app, db, login_manager
from server.forms import MainButtonsForm, LoginForm, RegistrationForm, ProfileUsernameForm, ProfilePasswordForm
from server.user import User
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from server.custom_paginated import CustomPaginated

@app.route('/')
@login_required
def index():
    form = MainButtonsForm()
    if 'paginated' not in session or session['paginated'] is None: #TODO delete this dummy paginated and dummy hints
        session['paginated'] = CustomPaginated(['A', 'B'], [['a1','b1'], ['a2','b2'], ['a3','b3']], 2).to_dict()
        session['hints'] = ['Hint A', 'Hint B', 'Hint C']
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

@login_manager.user_loader
def load_user(user_id):
    user_data = db.get_user_by_id(user_id)
    if user_data:
        # user_data = (id, username, email, password_hash, is_admin)
        return User(id=user_data[0], username=user_data[1], email=user_data[2], password_hash=user_data[3], is_admin=user_data[4])
    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user_data = db.get_user_by_username(form.username.data)

        if user_data:
            user = User(
                id=user_data[0],
                username=user_data[1],
                email=user_data[2],
                password_hash=user_data[3],
                is_admin=user_data[4]
            )

            if check_password_hash(user.password_hash, form.password.data):
                login_user(user, remember=form.remember_me.data)

                next_page = request.args.get('next')
                if not next_page or not next_page.startswith('/'):
                    next_page = url_for('index')
                return redirect(next_page)

        return render_template('login.html', form=form, login_error='Wrong username or password')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()

    if form.validate_on_submit():
        if db.get_user_by_username(form.username.data):
            return render_template('register.html', form=form, registration_error='Username already exists')

        hashed_password = generate_password_hash(form.password.data)
        new_user_id = db.add_user(form.username.data, form.email.data, hashed_password)

        if new_user_id:
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            return render_template('register.html', form=form, registration_error='Database error')

    return render_template('register.html', form=form)


@login_required
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form_username = ProfileUsernameForm()
    form_password = ProfilePasswordForm()

    if 'username' in request.form and form_username.validate_on_submit():
        new_username = form_username.username.data

        existing_user = db.get_user_by_username(new_username)
        if existing_user and existing_user[0] != current_user.id:
            flash('Це ім\'я вже зайняте іншим користувачем.', 'error')
        else:
            if db.update_username(current_user.id, new_username):
                flash('Ім\'я успішно оновлено!', 'success')
                return redirect(url_for('profile'))
            else:
                flash('Помилка бази даних.', 'error')

    if 'password' in request.form and form_password.validate_on_submit():
        hashed_pw = generate_password_hash(form_password.password.data)

        if db.update_password(current_user.id, hashed_pw):
            flash('Пароль успішно змінено!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Помилка при зміні пароля.', 'error')

    if request.method == 'GET':
        form_username.username.data = current_user.username

    return render_template(
        'profile.html',
        form_username=form_username,
        form_password=form_password
    )
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


@app.route('/toggle_favorite/<int:book_id>', methods=['POST'])
@login_required
def toggle_favorite(book_id):
    if db.is_book_favorite(current_user.id, book_id):
        db.remove_favorite(current_user.id, book_id)
        flash('Removed from favorites', 'info')
    else:
        db.add_favorite(current_user.id, book_id)
        flash('Added to favorites', 'success')

    return redirect(request.referrer or url_for('index'))


@app.route('/my_favorites')
@login_required
def my_favorites():
    fav_books = db.get_user_favorites(current_user.id)
    return render_template('favorites.html', books=fav_books)
