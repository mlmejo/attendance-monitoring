import click
from flask.cli import AppGroup
from werkzeug.security import generate_password_hash

from app.models import User
from app.services import db

cli = AppGroup('admin', short_help='Run administrator commands.')


@cli.command(help='Create an admin account.')
def create() -> None:
    user = User(
        name='Administrator',
        email='admin@example.com',
        password=generate_password_hash('password'),
        is_admin=True,
    )

    db.session.add(user)
    db.session.commit()

    click.echo('Admin created successfully.')
