import os

from flask import Blueprint, abort, render_template, request

from app.models import FacultyLoad, QRCode
from app.services import db

blueprint = Blueprint('instructors', __name__)


@blueprint.route('/my-schedules')
def schedules():
    return render_template('instructors/schedules.html')


@blueprint.route('/my-schedules/<int:faculty_load>')
def schedule_details(faculty_load):
    faculty_load = FacultyLoad.query.get_or_404(faculty_load)
    return render_template('schedules/show.html', faculty_load=faculty_load)


@blueprint.post('/qrcodes')
def create_qrcode():
    faculty_load_id = request.form.get('faculty_load_id')

    if not faculty_load_id:
        return abort(403)

    faculty_load = FacultyLoad.query.get_or_404(faculty_load_id)
    generated = QRCode(faculty_load_id=faculty_load.id)

    db.session.add(generated)
    db.session.commit()

    ip_addr = os.environ['IP_ADDRESS']
    url = f'http://{ip_addr}:5000/{generated.token}'

    return render_template('qrcode.html', url=url)
