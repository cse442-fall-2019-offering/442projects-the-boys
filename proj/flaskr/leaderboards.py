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
        friendFilter = False
        if 'friendFilter' in request.form:
            friendFilter = True
        print(friendFilter)
        if friendFilter:
            if criteria == "username":
                criteria = "user_name"
            elif criteria == "income":
                criteria = "income"
            elif criteria == "occupation":
                criteria = "field"
            elif criteria == "location":
                criteria = "location"
            print("SELECT * FROM friends WHERE friend_id = {}"
                " ORDER BY {}".format(session.get('user_id'), criteria))
            peoples = db.selectall(
                "SELECT * FROM friends WHERE friend_id = {}"
                " ORDER BY {}".format(session.get('user_id'), criteria)
            )
            print(peoples)
            for person in peoples:
                person["username"] = person["user_name"]
                person["occupation"] = person["field"]

        else:
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
