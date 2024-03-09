from flask_wtf.file import FileAllowed
from wtforms import DateField, EmailField, FileField, PasswordField, SelectField, StringField
from wtforms.validators import DataRequired, ValidationError

from app.forms import Form
from app.models import Course, User, Student


class StudentForm(Form):
    course_id = SelectField('Course')
    student_id = StringField('Student ID', validators=[DataRequired()])
    image = FileField(
        'Image registration',
        validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Must be an image.')],
    )
    last_name = StringField('Last name', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    middle_name = StringField('Middle name')
    gender = SelectField('Gender', choices=[
        ('male', 'Male'),
        ('female', 'Female'),
    ])
    birthdate = DateField('Birth date', validators=[DataRequired()])
    contact_number = StringField('Contact number', validators=[DataRequired()])
    year_level = SelectField('Year level', choices=[
        ('First year', 'First year'),
        ('Second year', 'Second year'),
        ('Third year', 'Third year'),
        ('Fourth year', 'Fourth year'),
    ])
    email = EmailField('Email address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course_id.choices = [
            (course.id, course.name) for course in Course.query.all()
        ]

    def validate_email(self, email) -> None:
        user = User.query.filter_by(email=email.data).first()

        if user and self.obj != user:
            raise ValidationError('The email has already been taken.')

    def validate_student_id(self, student_id) -> None:
        user = Student.query.filter_by(student_id=student_id.data).first()

        if user and self.obj != user:
            raise ValidationError('The student_id has already been taken.')


class TimeInForm(Form):
    image = FileField(
        'Face recognition',
        validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Must be an image.')],
    )
