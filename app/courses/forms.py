from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError

from app.forms import Form
from app.models import Course


class CourseForm(Form):
    name = StringField('Course name', validators=[DataRequired()])

    def validate_name(self, name) -> None:
        course = Course.query.filter_by(name=name.data).first()
        if course and course != self.obj:
            raise ValidationError('The name has already been taken')
