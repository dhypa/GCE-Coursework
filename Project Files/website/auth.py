from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, login_manager
from . import models, db
from .models import Users

auth = Blueprint('auth', __name__)

#LOGIN PAGE
@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method== 'POST':
        name=request.form.get('name')
        password = request.form.get('password')
        
        user= Users.query.filter_by(name=name).first()
        if user: 
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))

            else:
                flash('Incorrect details, try again', category='error')
                
                
            
    data=request.form

    return render_template('login.html')

#LOGOUT
@auth.route('/logout')
@login_required
def logout(): 
    logout_user()
    return redirect(url_for('auth.login'))



