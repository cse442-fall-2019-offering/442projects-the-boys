from flask import (Blueprint, flash, session, g, redirect, render_template, request, url_for)

import flaskr.db
from werkzeug.exceptions import abort

bp = Blueprint('profiles', __name__, url_prefix='/bio')


@bp.route('/profile' , methods = ['GET', 'POST'])
def profile():
    if g.user is None:
        return redirect(url_for("auth.login"))

    db = flaskr.db.Database()

    print(session.get('user_id'))
    expenses = db.selectall(

        "SELECT * FROM expense WHERE author_id = '{}'".format(session.get('user_id'))

    )

    if request.method == 'Post':
        name = request.form['fullName']
        occupation = request.form['occupation']
        age = request.form['age']
        location = request.form['location']
        income = request.form['income']
        error = None

        if not name:
            error = "Please enter your name!"
        if not occupation:
            error = "Please enter your occupation or field!"
        if not age:
            error = "Please enter your age!"
        if not location:
            error = "Please enter your Location!"
        if not income:
            error = "Please enter an estimate of your income value!"
        if error is not None:
            flash(error)

        db.insert(
            "INSERT INTO user (name, occupation, age, location, income ) VALUES ('"+name+"', '" + occupation + age +
            location + income+"')"
        )
        return redirect(url_for('profile.profiles'))




    # Will list all of a users expenses
    return render_template('profiles/profile.html', expenses=expenses)
