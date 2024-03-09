from wtforms import IntegerField, SelectField, SelectMultipleField, StringField
from wtforms.validators import DataRequired

from app.forms import Form
from app.models import Course


class SubjectForm(Form):
    course_ids = SelectMultipleField('Course')
    year_level = SelectField('Year level')
    semester = SelectField('Semester')
    descriptive_title = StringField('Descriptive title', validators=[DataRequired()])
    course_number = StringField('Course number', validators=[DataRequired()])
    lecture_hours = IntegerField('Lecture hours', validators=[DataRequired()])
    laboratory_hours = IntegerField('Laboratory hours', validators=[DataRequired()])
    units = IntegerField('Units', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.year_level.choices = [
            ('First year', 'First year'),
            ('Second year', 'Second year'),
            ('Third year', 'Third year'),
            ('Fourth year', 'Fourth year'),
        ]
        self.semester.choices = [
            ('First semester', 'First semester'),
            ('Second semester', 'Second semester'),
        ]
        self.course_ids.choices = [(course.id, course.name) for course in Course.query.all()]
