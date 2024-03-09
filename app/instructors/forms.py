from wtforms import EmailField, PasswordField, SelectField, StringField
from wtforms.validators import DataRequired, ValidationError

from app.forms import Form
from app.models import Department, User


class InstructorForm(Form):
    department_id = SelectField('Department')
    name = StringField('Instructor name', validators=[DataRequired()])
    email = EmailField('Email address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.department_id.choices = [
            (department.id, department.name) for department in Department.query.all()
        ]

    def validate_email(self, email) -> None:
        user = User.query.filter_by(email=email.data).first()

        if user and self.obj != user:
            raise ValidationError('The email has already been taken.')
