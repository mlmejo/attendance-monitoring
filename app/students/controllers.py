import os
import secrets
from io import BytesIO
from datetime import datetime

from flask import Blueprint, abort, flash, redirect, render_template, request
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from app.models import Attendance, QRCode
from app.services import db
from app.students.forms import TimeInForm

blueprint = Blueprint('students', __name__)


@blueprint.route('/<token>', methods=['GET', 'POST'])
@login_required
def time_in(token):
    qrcode = QRCode.query.filter_by(token=token).first()
    if not qrcode:
        return abort(404)

    form = TimeInForm()
    if form.validate_on_submit():
        student = current_user.student
        image = request.files['image']

        if student.verify_face(image):
            _, extension = os.path.splitext(secure_filename(image.filename))

            attendance = Attendance.query.filter_by(
                qrcode_id=qrcode.id,
                student_id=student.id,
            ).first()
            filename = ""

            if not attendance:
                filename = secure_filename(
                    f'{secrets.token_hex(16)}_{current_user.student.id}_TIME_IN' + extension
                )
                attendance = Attendance(
                    qrcode_id=qrcode.id,
                    student_id=student.id,
                    time_in=datetime.now(),
                    time_in_image=filename,
                )
                db.session.add(attendance)
            else:
                filename = secure_filename(
                    f'{secrets.token_hex(16)}_{current_user.student.id}_TIME_OUT' + extension
                )
                attendance.time_out = datetime.now()
                attendance.time_out_image = filename

            image.seek(0)
            image.save('profiles/' + filename)
            db.session.commit()

            flash(
                'Verification successfully. Your attendance has been recorded.',
                'success',
            )

            return redirect('/welcome')

        flash(
            'Face verification failed. Please upload an image of your face.',
            'danger',
        )

    return render_template(
        'students/time_in.html',
        faculty_load=qrcode.faculty_load,
        form=form,
    )


@blueprint.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')
