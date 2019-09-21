from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('leaderboards', __name__, url_prefix='/lead')


@bp.route('/main')
def leaderboard():
    return render_template('leaderboards/default_leader.html')
