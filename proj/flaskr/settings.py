from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
import flaskr.db
bp = Blueprint('settings', __name__, url_prefix='/settings')


@bp.route('/index', methods=['GET', 'POST'])
def settings():
    if g.user is None:
        return redirect(url_for("auth.login"))
    db = flaskr.db.Database()
    user = db.selectall(

        "SELECT * FROM user WHERE id = '{}'".format(session.get('user_id'))

    )

    if request.method == 'POST':
        name1 = request.form['fullname']
        username = request.form['username']
        anonymous = 0
        try:
            request.form['anonymous']
            anonymous = 1
        except :
            anonymous = 0

            db.insert(
                "UPDATE user SET name1 = '{}' WHERE id='{}' ".format(name1, session.get('user_id'))
            )
            db.insert(
                "UPDATE user SET username = '{}' WHERE id='{}' ".format(username, session.get('user_id'))
            )

            db.insert(
                "UPDATE user SET anonymous = '{}' WHERE id='{}' ".format(anonymous, session.get('user_id'))
            )



    return render_template('settings/index.html', user=user)
