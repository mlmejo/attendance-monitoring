from wtforms import StringField, SelectField, TimeField
from wtforms.validators import DataRequired

from app.forms import Form
from app.models import Instructor, Subject


class FacultyLoadForm(Form):
    instructor_id = SelectField()
    subject_id = SelectField()
    school_year = StringField(validators=[DataRequired()])
    semester = SelectField()
    room = StringField(validators=[DataRequired()])
    day = StringField(validators=[DataRequired()])
    time_start = TimeField(validators=[DataRequired()])
    time_end = TimeField(validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instructor_id.choices = [
            (instructor.id, instructor.user.name) for instructor in Instructor.query.all()
        ]
        self.subject_id.choices = [
            (subject.id, subject.descriptive_title) for subject in Subject.query.all()
        ]
        self.semester.choices = [
            ('1st semester', '1st semester'),
            ('2nd semester', '2nd semester'),
        ]
