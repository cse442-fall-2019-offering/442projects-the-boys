from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)

from werkzeug.exceptions import abort

bp = Blueprint('profiles', __name__, url_prefix='/bio')


@bp.route('/profile' , methods = ['GET', 'POST'])
def profile():
    if g.user is None:
        return redirect(url_for("auth.login"))
    return render_template('profiles/profile.html')
