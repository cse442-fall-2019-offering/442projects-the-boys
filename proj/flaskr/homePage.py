from flask import (Blueprint, flash, g, session, redirect, render_template, request, url_for)

from werkzeug.exceptions import abort
import flaskr.db
import datetime
bp = Blueprint('homePages', __name__)


@bp.route('/')
def homePage():
    if g.user is None:
        return redirect(url_for("auth.login"))

    db = flaskr.db.Database()

    print(session.get('user_id'))


    expenses = db.selectall(

        "SELECT * FROM expense WHERE author_id = '{}'"
        "ORDER BY category, cost".format(session.get('user_id'))

    )
    user = db.selectall(

        "SELECT * FROM user WHERE id = '{}'".format(session.get('user_id'))

    )
    friends = db.selectall(
        "SELECT * FROM friends WHERE friend_id= '{}'".format(session.get('user_id'))
    )
    numFriends= len(friends)

    now = datetime.datetime.now()
    total_expenses = { "daily": 0, "weekly": 0, "monthly": 0, "yearly": 0, "oneTime": 0, "total": 0 }
    total_category = { "Food": 0, "Utilities": 0, "Recreational": 0, "Medical": 0, "Rent / Mortgage": 0, "Phone": 0, "Vehicle": 0 , "Other": 0 }

    for index, expense in enumerate(expenses) :
        total_category[expense['category']] = total_category[expense['category']] + expense['cost']
        timeago = now -  expense['created']
        secs = timeago.total_seconds()
        days = round(secs//86400)
        hours = round((secs - days*86400)//3600)
        minutes = round((secs - days*86400 - hours*3600)//60)
        seconds = round(secs - days*86400 - hours*3600 - minutes*60)
        if expense['rate'] == 'Daily' :
            total_expenses['daily'] = total_expenses['daily'] + expense['cost']
        elif expense['rate'] == 'Weekly' :
            total_expenses['weekly'] = total_expenses['weekly'] + expense['cost']
        elif expense['rate'] == 'Monthly' :
            total_expenses['monthly'] = total_expenses['monthly'] + expense['cost']
        elif expense['rate'] == 'Yearly' :
            total_expenses['yearly'] = total_expenses['yearly'] + expense['cost']
        elif expense['rate'] == 'One Time' :
            total_expenses['oneTime'] = total_expenses['oneTime'] + expense['cost']
        if days == -1 :
            expense['timeago'] = 'Just created'
        else :
            expense['timeago'] = str(days) + " days " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds) + " seconds ago"
        expenses[index] = expense

    total_expenses['total'] = total_expenses['daily'] * 365 + total_expenses['weekly'] * 52 + total_expenses['monthly'] * 12 + total_expenses['yearly'] + total_expenses['oneTime']
    total = total_expenses['total'] // 12

    if request.method == 'POST':
        name1 = request.form['fullname']
        occupation = request.form['occupation']
        age = request.form['age']
        location = request.form['location']
        income = request.form['income']
        error = None
        anonymous = request.form['anonymous']
        if not name1:
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
        else:
            db.insert(
                "UPDATE user SET name1 = '{}' WHERE id='{}' ".format(name1, session.get('user_id'))
            )
            db.insert(
                "UPDATE user SET occupation = '{}' WHERE id='{}' ".format(occupation, session.get('user_id'))
            )
            db.insert(
                "UPDATE user SET age = '{}' WHERE id='{}' ".format(age, session.get('user_id'))
            )

            db.insert(
                "UPDATE user SET location = '{}' WHERE id='{}' ".format(location, session.get('user_id'))
            )
            db.insert(
                "UPDATE user SET income = '{}' WHERE id='{}' ".format(income, session.get('user_id'))
            )
            db.insert(
                "UPDATE user SET anonymous = '{}' WHERE id='{}' ".format(anonymous, session.get('user_id'))
            )
        return redirect(url_for('profiles.profile'))

    # Will list all of a users expenses
    if user[0]['income'] is None :
        user[0]['income'] = 0
    return render_template('homePages/homePage.html',infographics=infographics(total, user[0]['income'] // 12), total_category=total_category, expenses=expenses,total_expenses=total_expenses, user=user[0],friends=friends,numFriends=numFriends)

def infographics(spent, left) :
    infographicdata = []
    infographicdata.append(spent)
    infographicdata.append(left - spent)
    return infographicdata
