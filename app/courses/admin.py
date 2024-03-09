from flask import Blueprint, flash, redirect, render_template, request

from app.admin.decorators import admin_required
from app.courses.forms import CourseForm
from app.models import Course, Department
from app.services import db

admin = Blueprint('courses', __name__)


@admin.route('/departments/<int:department_id>/courses/create', methods=['GET', 'POST'])
@admin_required
def create(department_id):
    department = Department.query.get_or_404(department_id)
    form = CourseForm()

    if form.validate_on_submit():
        course = Course(
            department_id=department_id,
            name=form.name.data,
        )
        db.session.add(course)
        db.session.commit()

        flash('Course created successfully.', 'success')

        return redirect(f'/admin/departments/{department_id}/edit')

    return render_template('admin/courses/create.html', department=department, form=form)


@admin.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(course_id):
    course = Course.query.get_or_404(course_id)
    form = CourseForm(obj=course)

    if form.validate_on_submit():
        course.name = form.name.data
        db.session.commit()

        flash('Course updated successfully.', 'success')

        return redirect(f'/admin/departments/{course.department_id}/edit')

    return render_template('admin/courses/edit.html', course=course, form=form)


@admin.route('/courses/<int:course_id>/delete', methods=['GET', 'POST'])
@admin_required
def destroy(course_id):
    course = Course.query.get_or_404(course_id)

    if request.method == 'POST':
        department_id = course.department_id
        db.session.delete(course)
        db.session.commit()

        flash('Course deleted successfully.', 'success')

        return redirect(f'/admin/departments/{department_id}/edit')

    return render_template('admin/courses/delete.html', course=course)


@admin.route('/courses/<int:course_id>/subjects')
@admin_required
def courses(course_id):
    course = Course.query.get_or_404(course_id)
    year_levels = ['First year', 'Second year', 'Third year', 'Fourth year']
    semesters = ['First semester', 'Second semester']
    subjects = {}

    for year_level in year_levels:
        subjects[year_level] = {}

        for semester in semesters:
            subjects[year_level][semester] = course.subjects_by_term(year_level, semester)

    return render_template('admin/courses/_subjects.html', course=course, subjects=subjects)
