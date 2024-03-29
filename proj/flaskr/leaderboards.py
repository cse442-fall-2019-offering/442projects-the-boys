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
                criteria = "friends.user_name"
            elif criteria == "income":
                criteria = "friends.income"
            elif criteria == "occupation":
                criteria = "friends.field"
            elif criteria == "location":
                criteria = "friends.location"
            print("SELECT * FROM friends WHERE friend_id = {}"
                " ORDER BY {}".format(session.get('user_id'), criteria))
            peoples = db.selectall(
                "SELECT * FROM friends INNER JOIN user ON user.id=friends.user_id WHERE friend_id = {}"
                " ORDER BY {}".format(session.get('user_id'), criteria)
            )

            for person in peoples:
                person["username"] = person["user_name"]
                person["occupation"] = person["field"]
            print(peoples)
        else:
            peoples = db.selectall(
                "SELECT * FROM user WHERE occupation IS NOT NULL"
                " ORDER BY {}".format(criteria)
            )

        friends = db.selectall(
            "SELECT user_id FROM friends WHERE friend_id= {}"
            " ORDER BY income".format(session.get('user_id'))
        )

        for index, person in enumerate(peoples) :
            peoples[index]['isfriend'] = 0
            for friend in friends :
                if friend['user_id'] == person['id'] :
                    peoples[index]['isfriend'] = 1
        if "friends." in criteria:
            criteria = criteria.split(".")[1]
        if criteria == "user_name":
            criteria = "username"
        return render_template('leaderboards/default_leader.html', people=peoples, cat=criteria)

    peoples = db.selectall(
        "SELECT * FROM user WHERE occupation IS NOT NULL"
        " ORDER BY income"
    )

    friends = db.selectall(
        "SELECT user_id FROM friends WHERE friend_id= {}"
        " ORDER BY income".format(session.get('user_id'))
    )

    for index, person in enumerate(peoples) :
        peoples[index]['isfriend'] = 0
        for friend in friends :
            if friend['user_id'] == person['id'] :
                peoples[index]['isfriend'] = 1


    criteria = "income"

    return render_template('leaderboards/default_leader.html',friends=friends, people=peoples, cat=criteria)
