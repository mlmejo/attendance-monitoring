from flask import Blueprint, jsonify, render_template, request

from app.admin.decorators import admin_required
from app.faculty_loads.forms import FacultyLoadForm
from app.models import FacultyLoad, Instructor, Subject
from app.services import db

admin = Blueprint('faculty_loads', __name__)


@admin.route('/faculty-loads', methods=['GET', 'POST'])
@admin_required
def index():
    instructors = Instructor.query.all()

    if request.method == 'POST':
        form = FacultyLoadForm(request.form)

        if not form.validate():
            return jsonify(list(form.errors.items()))

        faculty_load = FacultyLoad(
            instructor_id=form.instructor_id.data,
            subject_id=form.subject_id.data,
            school_year=form.school_year.data,
            semester=form.semester.data,
            room=form.room.data,
            day=form.day.data,
            time_start=form.time_start.data,
            time_end=form.time_end.data,
        )

        db.session.add(faculty_load)
        db.session.commit()

        instructor = Instructor.query.get(form.instructor_id.data)
        subject = Subject.query.get(form.subject_id.data)

        return jsonify(
            f'{subject.descriptive_title} is added to {instructor.user.name}\'s load.'
        )

    return render_template(
        'admin/faculty_loads/index.html',
        instructors=instructors,
    )


@admin.delete('/faculty-loads')
@admin_required
def destroy():
    instructor_id = request.form.get('instructor_id', None)
    subject_id = request.form.get('subject_id', None)

    if not instructor_id:
        return jsonify(errors='The instructor_id field is required.')

    if not subject_id:
        return jsonify(errors='The subject_id field is required.')

    faculty_load = FacultyLoad.query.filter_by(
        instructor_id=instructor_id,
        subject_id=subject_id,
    ).first()

    instructor = faculty_load.instructor
    subject = faculty_load.subject

    db.session.delete(faculty_load)
    db.session.commit()

    return jsonify(
        f'{subject.descriptive_title} has been removed from {instructor.user.name}.'
    )


@admin.post('/faculty-loads/_table')
@admin_required
def table():
    instructor_id = request.form['instructor_id']

    if not instructor_id:
        return jsonify(error='The instructor_id field is required.')

    instructor = Instructor.query.get(instructor_id)
    subjects = Subject.query.all()

    return render_template(
        'admin/faculty_loads/_table.html',
        instructor=instructor,
        subjects=subjects,
    )
