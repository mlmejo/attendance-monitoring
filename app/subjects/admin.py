from flask import Blueprint, flash, redirect, render_template, request
from sqlalchemy.exc import IntegrityError

from app.admin.decorators import admin_required
from app.subjects.forms import SubjectForm
from app.models import Course, Subject
from app.services import db

admin = Blueprint('subjects', __name__)


@admin.route('/subjects', methods=['GET', 'POST'])
@admin_required
def index():
    courses = Course.query.all()
    return render_template('admin/subjects/index.html', courses=courses)


@admin.route('/subjects/create', methods=['GET', 'POST'])
@admin_required
def create():
    form = SubjectForm()

    if form.validate_on_submit():
        try:
            subject = Subject(
                year_level=form.year_level.data,
                semester=form.semester.data,
                descriptive_title=form.descriptive_title.data,
                course_number=form.course_number.data,
                lecture_hours=form.lecture_hours.data,
                laboratory_hours=form.laboratory_hours.data,
                units=form.units.data,
            )

            db.session.add(subject)

            for course_id in form.course_ids.data:
                course = Course.query.get(course_id)
                course.subjects.append(subject)
        except IntegrityError:
            form.course_ids.errors.append('This subject is already assigned to a selected course.')
        else:
            db.session.commit()
            flash('Subject created successfully.', 'success')
            return redirect('/admin/subjects')

    return render_template('admin/subjects/create.html', form=form)


@admin.route('/subjects/<int:subject_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    courses = Course.query.all()
    form = SubjectForm(obj=subject)

    if form.validate_on_submit():
        subject.descriptive_title = form.descriptive_title.data
        subject.course_number = form.course_number.data
        subject.lecture_hours = form.lecture_hours.data
        subject.laboratory_hours = form.laboratory_hours.data
        subject.units = form.units.data
        subject.courses = []

        for course_id in form.course_ids.data:
            course = Course.query.get(course_id)
            course.subjects.append(subject)

        db.session.commit()

        flash('Subject updated successfully.', 'success')

        return redirect('/admin/subjects')

    return render_template(
        'admin/subjects/edit.html',
        subject=subject,
        courses=courses,
        form=form,
    )


@admin.route('/subjects/<int:subject_id>/delete', methods=['GET', 'POST'])
@admin_required
def destroy(subject_id):
    subject = Subject.query.get_or_404(subject_id)

    if request.method == 'POST':
        db.session.delete(subject)
        db.session.commit()

        flash('Subject deleted successfully.', 'success')

        return redirect('/admin/subjects')

    return render_template('admin/subjects/delete.html', subject=subject)
