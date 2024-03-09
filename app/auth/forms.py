from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, ValidationError

from app.forms import Form
from app.models import User


class LoginForm(Form):
    email = EmailField('Email address', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class UserForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email address', validators=[DataRequired()])
    password = PasswordField('Password')

    def validate_email(self, email) -> None:
        user = User.query.filter_by(email=email.data).first()

        if user and self.obj != user:
            raise ValidationError('The email has already been taken.')
