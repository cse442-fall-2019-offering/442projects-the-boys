from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import flaskr.db
bp = Blueprint('leaderboards', __name__, url_prefix='/lead')


@bp.route('/main', methods = ['GET', 'POST'])
def leaderboard():
    db = flaskr.db.Database()

    #Currently only display people on leaderboards if their bio information is filled out

    if request.method == 'POST':
        criteria = request.form['criteria']
        peoples = db.selectall(
            "SELECT * FROM user WHERE occupation IS NOT NULL"
            " ORDER BY {}".format(criteria)
        )
        return render_template('leaderboards/default_leader.html', people=peoples, cat=criteria)

    peoples = db.selectall(
        "SELECT * FROM user WHERE occupation IS NOT NULL"
        " ORDER BY income"
    )
    criteria = "income"

    return render_template('leaderboards/default_leader.html', people=peoples, cat=criteria)
