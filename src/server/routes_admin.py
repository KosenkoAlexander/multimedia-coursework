from flask import render_template, redirect, url_for
from server import app, db
from flask_login import current_user, login_required
from server.user import User
from server.custom_paginated import CustomPaginated

@login_required
@app.route('/admin')
def admin():
    if not current_user.is_admin:
        return redirect(url_for('index'))
    return render_template('admin.html')
