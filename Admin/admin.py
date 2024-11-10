from flask import Blueprint, session, redirect, url_for, flash, request, render_template

admin_login = Blueprint('admin_login', __name__)

ADMIN_USERNAME = 'admin@administrator.ru'
ADMIN_PASSWORD = 'password'

def is_admin():
    return session.get("role") == "admin"

@admin_login.route('/admin/login', methods=['GET', 'POST'])
def admin_login_func():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['role'] = 'admin'
            flash('Logged in successfully as admin', 'success')
            return redirect('/swagger')
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('admin_login.html')

@admin_login.route('/admin/logout')
def admin_logout():
    session.pop('role', None)
    flash('Logged out successfully', 'info')
    return redirect(url_for('admin_login.admin_login_func'))
