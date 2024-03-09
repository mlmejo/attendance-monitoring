from flask import Blueprint, jsonify, render_template, request

from app.admin.decorators import admin_required
from app.models import FacultyLoad, Student
from app.schedules.forms import ScheduleForm
from app.services import db

admin = Blueprint('schedules', __name__)


@admin.route('/schedules', methods=['GET', 'POST'])
@admin_required
def index():
    students = Student.query.all()

    if request.method == 'POST':
        form = ScheduleForm(request.form)

        if not form.validate():
            return jsonify(list(form.errors.items()))

        faculty_load = FacultyLoad.query.get(form.faculty_load_id.data)
        student = Student.query.get(form.student_id.data)

        faculty_load.students.append(student)
        db.session.commit()

        return jsonify(f'{student.user.name}\'s study load changed.')

    return render_template(
        'admin/schedules/index.html',
        students=students,
    )


@admin.delete('/schedules')
@admin_required
def destroy():
    student_id = request.form.get('student_id', None)
    faculty_load_id = request.form.get('faculty_load_id', None)

    if not student_id:
        return jsonify(errors='The student_id field is required.')

    if not faculty_load_id:
        return jsonify(errors='The faculty_load_id field is required.')

    student = Student.query.get(student_id)
    faculty_load = FacultyLoad.query.get(faculty_load_id)

    faculty_load.students.remove(student)
    db.session.commit()

    return jsonify(
        f'{student.user.name} has been removed.'
    )
