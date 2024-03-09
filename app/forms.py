from flask_wtf import FlaskForm


class Form(FlaskForm):

    def __init__(self, obj=None, *args, **kwargs):
        super().__init__(obj=obj, *args, **kwargs)
        self.obj = obj
