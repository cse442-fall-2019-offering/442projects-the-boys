from flask import (Blueprint, flash, session, g, redirect, render_template, request, url_for)

from werkzeug.exceptions import abort

bp = Blueprint('profiles', __name__, url_prefix='/bio')

import flaskr.db


@bp.route('/profile' , methods = ['GET', 'POST'])
def profile():
    if g.user is None:
        return redirect(url_for("auth.login"))

    db = flaskr.db.Database()

    print(session.get('user_id'))
    expenses = db.selectall(

        "SELECT * FROM expense WHERE author_id = '{}'".format(session.get('user_id'))

    )
    # Will list all of a users expenses
    return render_template('profiles/profile.html', expenses=expenses)
