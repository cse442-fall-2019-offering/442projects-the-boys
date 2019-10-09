
import click
from flask import current_app, g
from flask.cli import with_appcontext

import pymysql
import flaskr.config


class Database:
    def __init__(self):
        host = flaskr.config.host
        user = flaskr.config.user
        password = flaskr.config.password
        db = flaskr.config.db
        self.con = pymysql.connect(host=host, user=user, password=password, database=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def insert(self, statement) :
        res = self.cur.execute(statement)
        self.con.commit()
        return res

    def select(self, statement):
        self.cur.execute(statement)
        result = self.cur.fetchone()
        return result

    def selectall(self, statement):
        self.cur.execute(statement)
        result = self.cur.fetchall()
        return result

    def close_db(self, e=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()


    def init_db(self):
        db = get_db()
        with current_app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(Database.close_db)
    app.cli.add_command(init_db_command)
