from flask import Blueprint, redirect, render_template, request
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.auth.forms import LoginForm, UserForm
from app.models import User
from app.services import db

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')

            if next_page:
                return redirect(next_page)

            if user.is_instructor:
                return redirect('/my-schedules')

            if user.is_student:
                return redirect('/welcome')

        form.email.errors.append('The provided credentials do not match our records.')

    return render_template('auth/login.html', form=form)


@blueprint.post('/logout')
def logout():
    logout_user()
    return redirect('/')


@blueprint.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UserForm(obj=current_user)

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        user.name = form.name.data
        user.email = email
        if password:
            user.password = generate_password_hash(password)

        db.session.commit()

        if current_user.is_admin:
            return redirect('/admin')
        elif current_user.is_instructor:
            return redirect('/my-schedules')
        elif current_user.is_student:
            return redirect('/welcome')

    return render_template('auth/profile.html', form=form)
