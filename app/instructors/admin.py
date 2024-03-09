from flask import Blueprint, flash, redirect, render_template, request
from werkzeug.security import generate_password_hash

from app.admin.decorators import admin_required
from app.instructors.forms import InstructorForm
from app.models import Department, Instructor, User
from app.services import db

admin = Blueprint('instructors', __name__)


@admin.route('/instructors')
@admin_required
def index():
    instructors = Instructor.query.all()
    return render_template('admin/instructors/index.html', instructors=instructors)


@admin.route('/instructors/create', methods=['GET', 'POST'])
@admin_required
def create():
    form = InstructorForm()

    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data),
            is_instructor=True,
        )
        instructor = Instructor(user=user, department_id=form.department_id.data)

        db.session.add_all([user, instructor])
        db.session.commit()

        flash('Instructor created successfully.', 'success')

        return redirect('/admin/instructors')

    return render_template('admin/instructors/create.html', form=form)


@admin.route('/instructors/<int:instructor_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(instructor_id):
    instructor = Instructor.query.get_or_404(instructor_id)
    departments = Department.query.all()
    form = InstructorForm(obj=instructor.user)

    if form.validate_on_submit():
        instructor.department_id = form.department_id.data
        instructor.user.name = form.name.data
        instructor.user.email = form.email.data

        db.session.commit()

        flash('Instructor updated successfully.', 'success')

        return redirect('/admin/instructors')

    return render_template(
        'admin/instructors/edit.html',
        instructor=instructor,
        departments=departments,
        form=form,
    )


@admin.route('/instructors/<int:instructor_id>/delete', methods=['GET', 'POST'])
@admin_required
def destroy(instructor_id):
    instructor = Instructor.query.get_or_404(instructor_id)

    if request.method == 'POST':
        db.session.delete(instructor.user)
        db.session.commit()

        flash('Instructor deleted successfully.', 'success')

        return redirect('/admin/instructors')

    return render_template('admin/instructors/delete.html', instructor=instructor)
