from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError

from app.forms import Form
from app.models import Department


class DepartmentForm(Form):
    name = StringField('Department name', validators=[DataRequired()])

    def validate_name(self, name) -> None:
        department = Department.query.filter_by(name=name.data).first()
        if department and department != self.obj:
            raise ValidationError('The name has already been taken.')
