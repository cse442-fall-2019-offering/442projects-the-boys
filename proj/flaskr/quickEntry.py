from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('quickEntry', __name__, url_prefix='/quick')


@bp.route('/entry')
def quickEntry():
    if g.user is None:
        return redirect(url_for("auth.login"))
    return render_template('quickEntry/default_entry.html')
