from flask import render_template, redirect, url_for, request, flash
from server import app, db
from flask_login import current_user, login_required
from server.user import User
from server.custom_paginated import CustomPaginated
from werkzeug.security import generate_password_hash

@app.route('/admin')
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

    return render_template('admin.html',
                           authors=authors,
                           genres=genres,
                           shops=shops,
                           libraries=libraries,
                           books=books,
                           users=users,
                           active_tab=active_tab)

@app.route('/add_book', methods=['POST'])
@login_required
def add_book():
    if not current_user.is_admin:
        return redirect(url_for('index'))

    try:
        name = request.form.get('name')
        pages = int(request.form.get('pages'))

        authors_ids = [int(x) for x in request.form.getlist('authors')]
        genres_ids = [int(x) for x in request.form.getlist('genres')]

        location_type = request.form.get('location_type')  # 'none', 'shop', 'library'
        link_url = request.form.get('link')
        if not link_url or link_url.strip() == "":
            link_url = None

        book_id = db.create_book(name, pages)

        if book_id:
            db.link_authors_to_book(book_id, authors_ids)
            db.link_genres_to_book(book_id, genres_ids)

            if location_type == 'shop':
                shop_id = int(request.form.get('shop_id'))
                price_val = request.form.get('price')
                price = float(price_val) if price_val else 0.0

                db.add_book_to_shop(book_id, shop_id, price, link_url)

            elif location_type == 'library':
                library_id = int(request.form.get('library_id'))
                db.add_book_to_library(book_id, library_id, link_url)

            flash(f'The book "{name}" added successfully!', 'success')
        else:
            flash('Error', 'error')

    except Exception as e:
        flash(f'Error: {e}', 'error')
        print(f"DEBUG ERROR: {e}")

    return redirect(url_for('admin', tab='add-book'))

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