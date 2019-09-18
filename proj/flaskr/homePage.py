from flask import (Blueprint, flash, g, redirect, render_template, request, url_for)

from werkzeug.exceptions import abort

bp = Blueprint('homePages', __name__, url_prefix='/lead')


@bp.route('/home')
def homePage():
    return render_template('homePages/homePage.html')
