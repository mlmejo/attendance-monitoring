import os

from flask import Blueprint, flash, redirect, render_template, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from app.admin.decorators import admin_required
from app.models import Course, FacultyLoad, Student, User
from app.services import db
from app.students.forms import StudentForm

admin = Blueprint('students', __name__)


@admin.route('/students')
@admin_required
def index():
    students = Student.query.all()
    return render_template('admin/students/index.html', students=students)


@admin.route('/students/create', methods=['GET', 'POST'])
@admin_required
def create():
    form = StudentForm()

    if form.validate_on_submit():
        name = f'{form.first_name.data} {form.middle_name.data} {form.last_name.data}'
        user = User(
            name=name,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            is_student=True,
        )
        student = Student(
            user=user,
            course_id=form.course_id.data,
            student_id=form.student_id.data,
            first_name=form.first_name.data,
            middle_name=form.middle_name.data,
            gender=form.gender.data,
            birthdate=form.birthdate.data,
            contact_number=form.contact_number.data,
            last_name=form.last_name.data,
            year_level=form.year_level.data,
        )

        image = request.files['image']
        _, extension = os.path.splitext(secure_filename(image.filename))
        filename = secure_filename(f'STUDENT_{student.id}_PROFILE' + extension)
        student.image = filename
        image.save('profiles/' + filename)

        db.session.add_all([user, student])
        db.session.commit()

        flash('Student created successfully.', 'success')

        return redirect('/admin/students')

    print(form.errors.items())

    return render_template('admin/students/create.html', form=form)


@admin.route('/students/<int:student_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(student_id):
    student = Student.query.get_or_404(student_id)
    courses = Course.query.all()
    form = StudentForm(obj=student)

    form.email.data = student.user.name
    form.password.data = student.user.password

    if form.validate_on_submit():
        image = request.files['image']

        if image:
            _, extension = os.path.splitext(secure_filename(image.filename))
            filename = secure_filename(f'STUDENT_{student.id}_PROFILE' + extension)
            student.image = filename
            image.save('profiles/' + filename)

        name = f'{form.first_name.data} {form.middle_name.data} {form.last_name.data}'

        student.student_id = form.student_id.data
        student.course_id = form.course_id.data
        student.user.name = name
        student.user.email = form.email.data

        student.first_name = form.first_name.data
        student.middle_name = form.middle_name.data
        student.last_name = form.last_name.data
        student.gender = form.gender.data
        student.birthdate = form.birthdate.data
        student.year_level = form.year_level.data

        db.session.commit()

        flash('Student updated successfully.', 'success')

        return redirect('/admin/students')

    return render_template(
        'admin/students/edit.html',
        student=student,
        courses=courses,
        form=form,
    )


@admin.route('/students/<int:student_id>/delete', methods=['GET', 'POST'])
@admin_required
def destroy(student_id):
    student = Student.query.get_or_404(student_id)

    if request.method == 'POST':
        db.session.delete(student.user)
        db.session.commit()

        flash('Student deleted successfully.', 'success')

        return redirect('/admin/students')

    return render_template('admin/students/delete.html', student=student)


@admin.route('/students/<student_id>/schedules')
@admin_required
def schedules(student_id):
    student = Student.query.get_or_404(student_id)
    faculty_loads = FacultyLoad.query.all()

    return render_template(
        'admin/students/schedules.html',
        student=student,
        faculty_loads=faculty_loads,
    )
