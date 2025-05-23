from flask import Blueprint, session, redirect, url_for, flash, request, render_template
from flask_jwt_extended import create_access_token

admin_login = Blueprint('admin_login', __name__)

ADMIN_USERNAME = 'admin@administrator.ru'
ADMIN_PASSWORD = 'password'
admin_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczMTQzMjkwMSwianRpIjoiYjliZjFjODgtNWMxMC00MzVhLWIzZDAtZWU1YTU5MjUxNzQ0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzMxNDMyOTAxLCJjc3JmIjoiNmIwY2JiMmUtMjA0Mi00MGQ1LWEwMDgtZWM5NzJhMTg1MmRmIiwicm9sZV9pZCI6ImFkbWluIiwiaXNfYWRtaW4iOnRydWUsImxvZ2luIjoiYWRtaW4ifQ.WGCdo7-NyLT-o3c9b-sstXpTfIEX2uat3ufkIlrKRWQ'

def is_admin():
    return session.get("role") == "admin"

def get_admin_token():
    admin_token = create_access_token(
        identity="admin", 
        additional_claims={
            "role_id": "admin",
            "is_admin": True,
            "login": "admin",
        },
        expires_delta=False
    )
    return admin_token

@admin_login.route('/admin/login', methods=['GET', 'POST'])
def admin_login_func():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['role'] = 'admin'
            admin_token = get_admin_token()
            print(admin_token)
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