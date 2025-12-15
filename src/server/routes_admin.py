from flask import render_template, redirect, url_for, request, flash
from server import app, db
from server.forms import BookForm
from flask_login import current_user, login_required
from server.user import User
from server.custom_paginated import CustomPaginated
from werkzeug.security import generate_password_hash


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        return redirect(url_for('index'))

    authors = db.get_all_authors()
    genres = db.get_all_genres()
    shops = db.get_all_shops()
    libraries = db.get_all_libraries()
    books = db.get_all_books()
    users = db.get_all_users()
    active_tab = request.args.get('tab', 'add-book')
    
    form = BookForm() 

    form.authors.choices = [(a[0], f"{a[1]} {a[2]}") for a in authors]
    form.genres.choices = [(g[0], g[1]) for g in genres]
    form.shops.choices = [(s[0], s[1]) for s in shops]
    form.libraries.choices = [(l[0], l[1]) for l in libraries]

    book_id = request.args.get('book_id')
    if form.validate_on_submit():
        add_book(form, book_id)
        return redirect(url_for("admin", tab='add-book'))

    book_id = request.args.get("book_id", type=int)
    if book_id:
        book_name, authors_ids, genres_ids, shops_ids, libraries_ids = db.get_book_magic(book_id)
        # print(db.get_book_magic(book_id))
        if book_name:
            # this is the price of no ORM
            form.name.data = book_name
            form.authors.data = authors_ids
            form.genres.data =  genres_ids
            form.shops.data = shops_ids
            form.libraries.data = libraries_ids

    return render_template('admin.html',
                           form = form,
                           authors=authors,
                           genres=genres,
                           shops=shops,
                           libraries=libraries,
                           books=books,
                           users=users,
                           active_tab=active_tab)


# @app.route('/add_book', methods=['POST'])
# @login_required
def add_book(form: BookForm, book_id):  # book id = None if new book
    try:
        book_name = form.name.data
        authors_ids = form.authors.data
        genres_ids = form.genres.data
        shops_ids = form.shops.data
        libraries_ids = form.libraries.data

        if not book_id:
            # New book
            book_id = db.create_book(book_name, 0)  # pages literally make no sence. substitute with 0 for now
            if not book_id:
                flash('Error', 'error')
                return           

        db.change_book_magic(book_id, book_name, authors_ids, genres_ids, shops_ids, libraries_ids)
        # db.add_book_to_shop

        flash(f'The book "{book_name}" added successfully!', 'success')
        
    except Exception as e:
        flash(f'Error: {e}', 'error')
        print(f"DEBUG ERROR: {e}")


@app.route('/add_author', methods=['POST'])
@login_required
def add_author():
    if not current_user.is_admin: return redirect(url_for('index'))

    try:
        name = request.form.get('name')
        surname = request.form.get('surname')

        book_ids = [int(x) for x in request.form.getlist('books')]

        author_id = db.create_author(name, surname)

        if author_id:
            if book_ids:
                db.link_books_to_author(author_id, book_ids)

            flash(f'Author {name} {surname} added successfully!', 'success')
        else:
            flash('Error creating author.', 'error')

    except Exception as e:
        flash(f'System Error: {e}', 'error')
        print(e)

    return redirect(url_for('admin', tab='add-author'))


@app.route('/add_user', methods=['POST'])
@login_required
def add_user_route():

    if not current_user.is_admin:
        return redirect(url_for('index'))

    try:

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        is_admin = True if request.form.get('is_admin') else False

        password_hash = generate_password_hash(password)

        new_id = db.add_user(username, email, password_hash, is_admin)

        if new_id:
            flash(f'User {username} created successfully!', 'success')
        else:
            flash('Error: Username or Email might already exist.', 'error')

    except Exception as e:
        flash(f'System Error: {e}', 'error')
        print(f"Error adding user: {e}")

    return redirect(url_for('admin', tab='manage-users'))

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin: return redirect(url_for('index'))

    if user_id == current_user.id:
        flash('You can not delete yourself!', 'error')
        return redirect(url_for('admin', tab='manage-users'))

    db.delete_user(user_id)
    flash('User deleted.', 'success')
    return redirect(url_for('admin', tab='manage-users'))

@app.route('/toggle_admin/<int:user_id>', methods=['POST'])
@login_required
def toggle_admin(user_id):
    if not current_user.is_admin: return redirect(url_for('index'))

    if user_id == current_user.id:
        flash('You can`t change your admin rights!', 'error')
        return redirect(url_for('admin', tab='manage-users'))

    db.change_user_is_admin(user_id)
    flash('Success.', 'success')
    return redirect(url_for('admin', tab='manage-users'))


@app.route('/delete_book/<int:book_id>', methods=['POST'])
@login_required
def delete_book_route(book_id):
    if not current_user.is_admin: return redirect(url_for('index'))

    db.delete_book(book_id)
    flash('Book deleted successfully.', 'success')

    return redirect(url_for('admin', tab='add-book'))


@app.route('/delete_author/<int:author_id>', methods=['POST'])
@login_required
def delete_author_route(author_id):
    if not current_user.is_admin: return redirect(url_for('index'))

    db.delete_author(author_id)
    flash('Author deleted successfully.', 'success')

    return redirect(url_for('admin', tab='add-author'))