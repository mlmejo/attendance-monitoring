from flask import Blueprint, abort, render_template
from flask_login import current_user

blueprint = Blueprint('pages', __name__)


@blueprint.route('/profile')
def profile():
    return render_template('pages/profile.html')
