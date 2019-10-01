from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('settings', __name__, url_prefix='/settings')


@bp.route('/index')
def settings():
    if g.user is None:
        return redirect(url_for("auth.login"))
    return render_template('settings/index.html')
