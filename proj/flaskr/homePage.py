from flask import (Blueprint, flash, g, redirect, render_template, request, url_for, session)
import flaskr
import datetime

from werkzeug.exceptions import abort

bp = Blueprint('homePages', __name__)


@bp.route('/')
def homePage():
    db = flaskr.db.Database()

    print(session.get('user_id'))

    expenses = db.selectall(

        "SELECT * FROM expense"
        " ORDER BY created desc, cost limit 12"

    )
    dateconverter(expenses)
    peoples = db.selectall(
        "SELECT * FROM user WHERE occupation IS NOT NULL"
    )
    id_to_person = {}
    topid = 0
    for dicts in peoples:
        topid = max(topid, dicts['id'])
    for i in range(topid+1):
        id_to_person[i] = "Unknown"
    for dicts in peoples:
        id_to_person[dicts['id']] = dicts['username']
    return render_template('homePages/homePage.html', expenses=expenses, peoples=id_to_person)


def dateconverter(expenses):

    now = datetime.datetime.now()
    total_expenses = {"daily": 0, "weekly": 0, "monthly": 0, "yearly": 0, "oneTime": 0, "total": 0}
    total_category = {"Food": 0, "Utilities": 0, "Recreational": 0, "Medical": 0, "Rent / Mortgage": 0, "Phone": 0,
                      "Vehicle": 0, "Other": 0}

    for index, expense in enumerate(expenses):
        timeago = now - expense['created']
        secs = timeago.total_seconds()
        days = round(secs // 86400)
        hours = round((secs - days * 86400) // 3600)
        minutes = round((secs - days * 86400 - hours * 3600) // 60)
        seconds = round(secs - days * 86400 - hours * 3600 - minutes * 60)
        if days == -1:
            expense['timeago'] = 'Just created'
        else:
            expense['timeago'] = str(days) + " days " + str(hours) + " hours " + str(minutes) + " minutes " + str(
                seconds) + " seconds ago"
        expenses[index] = expense
