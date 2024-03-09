from datetime import datetime, timedelta

from flask import Blueprint, render_template, request
from flask_login import login_required
from sqlalchemy import func

from app.models import FacultyLoad, QRCode

blueprint = Blueprint('schedules', __name__)


@blueprint.route('/schedules/<int:schedule_id>/attendance')
@login_required
def attendance(schedule_id):
    schedule = FacultyLoad.query.get_or_404(schedule_id)

    return render_template(
        'schedules/attendance.html',
        title=f'Attendance Records',
        schedule=schedule,
    )


@blueprint.route('/schedules/<int:schedule_id>/attendance/_table')
@login_required
def attendance_table(schedule_id):
    date_target = request.args.get('date')

    if not date_target:
        date_target = datetime.today().date()
    else:
        date_target = datetime.strptime(date_target, '%m/%d/%Y').date()

    qrcode = QRCode.query.filter(
        func.DATE(QRCode.created_at)==date_target,
        FacultyLoad.id==schedule_id,
    ).first()
    records = []

    if qrcode:
        expected_datetime = datetime.combine(
            qrcode.created_at.date(),
            qrcode.faculty_load.time_start,
        )
        late_threshold = expected_datetime + timedelta(minutes=15)

        records = qrcode.attendance
        for entry in records:
            if entry.time_in.time() > late_threshold.time():
                entry.tardy_status = "Late"
            else:
                entry.tardy_status = "Present"

    return render_template('schedules/_table.html', records=records)
