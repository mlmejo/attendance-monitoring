from wtforms import IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError

from app.forms import Form
from app.models import FacultyLoad, Student


class ScheduleForm(Form):
    student_id = SelectField()
    faculty_load_id = IntegerField(validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.student_id.choices = [
            (student.id, student.user.name) for student in Student.query.all()
        ]

    def validate_faculty_load_id(self, faculty_load_id) -> None:
        faculty_load = FacultyLoad.query.get(faculty_load_id.data)

        if not faculty_load:
            raise ValidationError('The selected faculty_load_id is invalid.')
