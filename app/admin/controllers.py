from flask import Blueprint, abort, jsonify, redirect, render_template, request
from flask_login import current_user, login_user
from werkzeug.security import check_password_hash

from app.auth.forms import LoginForm
from app.admin.decorators import admin_required
from app.models import FacultyLoad, Instructor, User

blueprint = Blueprint(
    name='admin',
    import_name=__name__,
    url_prefix='/admin',
    template_folder='templates',
)


@blueprint.route('/dashboard', methods=['GET', 'POST'])
@admin_required
def dashboard():
    school_years = (FacultyLoad
                    .query
                    .with_entities(FacultyLoad.school_year)
                    .order_by(FacultyLoad.school_year.desc()).all())

    if request.method == 'POST':
        school_year = request.form.get('school_year')
        if not school_year:
            return jsonify('The school_year field is required.')

        semester = request.form.get('semester')
        if not semester:
            return jsonify('The semester field is required.')

        faculty_load = FacultyLoad.query.filter_by(
            school_year=school_year,
            semester=semester,
        ).first()

        if not faculty_load:
            return render_template(
                'admin/_graphs.html',
                notFound=True,
            )

        total_enrolled = len(faculty_load.students)

        return render_template(
            'admin/_graphs.html',
            total_enrolled=total_enrolled,
            school_year=faculty_load.school_year,
        )

    school_years = [school_year[0] for school_year in school_years]
    students = []

    for school_year in school_years:
        faculty_load = FacultyLoad.query.filter_by(school_year=school_year).first()
        students.append(len(faculty_load.students))

    instructors = Instructor.query.all()

    return render_template(
        'admin/dashboard.html',
        school_years=school_years,
        students=students,
        instructors=instructors,
    )


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/admin')

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user.is_admin:
            return abort(403)

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect('/admin/dashboard')
        else:
            form.email.errors.append('The provided credentials do not match our records.')

    return render_template('admin/login.html', form=form)


from app.departments.admin import admin as departments_admin
from app.courses.admin import admin as courses_admin
from app.subjects.admin import admin as subjects_admin
from app.instructors.admin import admin as instructors_admin
from app.students.admin import admin as students_admin
from app.faculty_loads.admin import admin as faculty_loads_admin
from app.schedules.admin import admin as schedules_admin

blueprint.register_blueprint(departments_admin)
blueprint.register_blueprint(courses_admin)
blueprint.register_blueprint(subjects_admin)
blueprint.register_blueprint(instructors_admin)
blueprint.register_blueprint(students_admin)
blueprint.register_blueprint(faculty_loads_admin)
blueprint.register_blueprint(schedules_admin)

blueprint.add_url_rule('/', 'dashboard')
