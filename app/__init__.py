import os

from flask import Flask, redirect, send_from_directory
from flask import current_app

from app.admin.cli import cli as admin_cli
from app.services import csrf, db, login_manager, migrate, qrcode


def index():
    return redirect('/auth/login')

def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOADS_FOLDER'], filename)


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ['SECRET_KEY'],
        SQLALCHEMY_DATABASE_URI='sqlite:///database.sqlite',
        UPLOADS_FOLDER=os.path.join(os.getcwd(), 'profiles')
    )

    csrf.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app)
    qrcode.init_app(app)

    app.cli.add_command(admin_cli)

    from app.auth.controllers import blueprint as auth_blueprint
    from app.admin.controllers import blueprint as admin_bluepint
    from app.instructors.controllers import blueprint as instructors_blueprint
    from app.students.controllers import blueprint as students_blueprint
    from app.schedules.controllers import blueprint as schedules_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(admin_bluepint)
    app.register_blueprint(instructors_blueprint)
    app.register_blueprint(students_blueprint)
    app.register_blueprint(schedules_blueprint)

    app.add_url_rule('/', view_func=index)
    app.add_url_rule('/uploads/<filename>', view_func=uploaded_file)

    return app
