from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import flaskr.db
import datetime
import random


from werkzeug.exceptions import abort

bp = Blueprint('quickEntry', __name__, url_prefix='/quick')


@bp.route('/entry', methods = ['GET', 'POST'])
def quickEntry():
    if g.user is None:
        return redirect(url_for("auth.login"))

    db = flaskr.db.Database()

    print(session.get('user_id'))

    #random number for tip gen range should correspond to the range of tip_ids in database 
    randId = random.randint(1, 9)

    #gets a random tip
    tips = db.select(
        "SELECT * FROM tips WHERE tip_id = '{}'".format(randId)
    )


    expenses = db.selectall(

        "SELECT * FROM expense WHERE author_id = '{}'"
        "ORDER BY category, cost".format(session.get('user_id'))

    )
    user = db.selectall(

        "SELECT * FROM user WHERE id = '{}'".format(session.get('user_id'))

    )

    now = datetime.datetime.now()
    total_expenses = { "daily": 0, "weekly": 0, "monthly": 0, "yearly": 0, "oneTime": 0, "total": 0 }

    for index, expense in enumerate(expenses) :
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
    if request.method == 'POST':

        category = request.form['category']
        title = request.form['title']
        cost = request.form['cost']
        rate = request.form['rate']
        error = None

        if not title:
            error = "Category required"
        if not title:
            error = "Expense name required"
        if not cost:
            error = "Cost required"
        if not rate:
            error = "Rate Required"
        if error is not None:
            flash(error)
        print(db.insert(
            "INSERT INTO expense (title, cost, author_id, category, rate) VALUES "
            "('" + title + "', '" + str(cost) + "', '" + str(g.user['id']) + "', '" + category + "', '" + rate + "')"
        ))
        return redirect(url_for('quickEntry.quickEntry'))
    if user[0]['income'] is None:
        user[0]['income'] = 0
    return render_template('quickEntry/default_entry.html', expenses=expenses, total_expenses=total_expenses, user=user[0],tips = tips)


# for delete button for each expense on the quickEntry page
# when clicked it deletes the expense from the database
@bp.route('/delete/<expense_id>', methods=['POST'])
def deleteEntry(expense_id):
    if g.user is None:
        return redirect(url_for("auth.login"))

    db = flaskr.db.Database()
    if request.method == 'POST':
        db.insert(
            "DELETE FROM expense WHERE id = '{}'".format(expense_id)
        )

    return redirect(url_for('quickEntry.quickEntry'))

# for edit expense button for each expense on quickEntry page
# when clicked user is redirected to a new page where they can edit an expense


@bp.route('/edit/<expense_id>/<category>/<title>/<cost>/<rate>', methods = ['GET', 'POST'])
def editExpense(expense_id, category, title, cost, rate):
    if g.user is None:
        return redirect(url_for("auth.login"))

    if request.method == 'POST':
        return redirect(url_for("quickEntry.finishEdit", expense_id=expense_id, expense_category=category,
                                expense_title=title, expense_cost=cost, expense_rate=rate))


# page for editing expense once edit expense button is clicked it updates the database

@bp.route('finishEdit/<expense_id>/<expense_category>/<expense_title>/<expense_cost>/<expense_rate>',
          methods=['GET', 'POST'])
def finishEdit(expense_id, expense_category, expense_title, expense_cost, expense_rate):
    if g.user is None:
        return redirect(url_for("auth.login"))
    if request.method == 'POST':
        category = request.form['category']
        title = request.form['title']
        cost = request.form['cost']
        rate = request.form['rate']
        error = None

        if not category:
            error = "Category Required"
        if not title:
            error = "Expense name required"
        if not cost:
            error = "Cost required"
        if not rate:
            error = "Rate required"
        if error is not None:
            flash(error)
        db = flaskr.db.Database()
        db.insert(
            "UPDATE expense SET title = '{}' , cost= '{}' , category = '{}', rate = '{}' WHERE id='{}' "
            .format(title, cost, category, rate, expense_id)
        )
        return redirect(url_for('quickEntry.quickEntry'))

    return render_template('quickEntry/edit_entry.html', expense_category=expense_category, expense_title=expense_title,
                           expense_cost=expense_cost, expense_rate=expense_rate)
