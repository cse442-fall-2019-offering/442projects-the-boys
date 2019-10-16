from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import flaskr.db
from werkzeug.exceptions import abort

bp = Blueprint('quickEntry', __name__, url_prefix='/quick')


@bp.route('/entry', methods = ['GET', 'POST'])
def quickEntry():
    if g.user is None:
        return redirect(url_for("auth.login"))

    db = flaskr.db.Database()

    print(session.get('user_id'))
    expenses = db.selectall(

        "SELECT * FROM expense WHERE author_id = '{}'".format(session.get('user_id'))

    )
    if request.method == 'POST':

        title = request.form['title']
        cost = request.form['cost']
        error = None

        if not title:
            error = "Expense name required"
        if not cost:
            error = "Cost required"
        if error is not None:
            flash(error)
        print(db.insert(
            "INSERT INTO expense (title, cost, author_id) VALUES "
            "('" + title + "', '" + str(cost) + "', '" + str(g.user['id']) + "')"
        ))
        return redirect(url_for('quickEntry.quickEntry'))

    return render_template('quickEntry/default_entry.html', expenses=expenses)



#for delete button for each expense on the quickEntry page
#when clicked it deletes the expense from the database
@bp.route('/delete/<expense_id>', methods = ['POST'])
def deleteEntry(expense_id):
    if g.user is None:
        return redirect(url_for("auth.login"))

    db = flaskr.db.Database()
    if request.method == 'POST':
        db.insert(
            "DELETE FROM expense WHERE id = '{}'".format(expense_id)
        )

    return redirect(url_for('quickEntry.quickEntry'))
#for edit expense button for each expense on quickEntry page
#when clicked user is redirected to a new page where they can edit an expense
@bp.route('/edit/<expense_id>/<title>/<cost>',methods = ['GET','POST'])
def editExpense(expense_id,title,cost):
    if g.user is None:
        return redirect(url_for("auth.login"))

    if request.method == 'POST':
       return redirect(url_for("quickEntry.finishEdit", expense_id=expense_id,expense_title=title,expense_cost=cost))




#page for editing expense once edit expense button is clicked it updates the database

@bp.route('finishEdit/<expense_id>/<expense_title>/<expense_cost>',methods=['GET','POST'])
def finishEdit(expense_id,expense_title,expense_cost):
    if g.user is None:
        return redirect(url_for(("auth.login")))
    if request.method == 'POST':
        title = request.form['title']
        cost = request.form['cost']
        error = None

        if not title:
            error = "Expense name required"
        if not cost:
            error = "Cost required"
        if error is not None:
            flash(error)
        db = flaskr.db.Database()
        db.insert(
            "UPDATE expense SET title = '{}' , cost= '{}' WHERE id='{}' ".format(title,cost,expense_id)
        )
        return redirect(url_for('quickEntry.quickEntry'))

    return render_template('quickEntry/edit_entry.html',expense_title=expense_title,expense_cost=expense_cost)