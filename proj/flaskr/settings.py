from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('settings', __name__, url_prefix='/settings')


@bp.route('/index')
def settings():
    return render_template('settings/index.html')
