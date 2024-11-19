from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from app import db
from flask import  render_template,flash,redirect, request,url_for
import sqlalchemy as sqla

from app.main import main_blueprint as bp_main
from app.main.models import Section,Position


@bp_main.route('/', methods=['GET'])
@bp_main.route('/index', methods=['GET'])
@login_required
def index():
    if current_user.user_type == 'Student':
        return redirect(url_for('main.student.index'))
    elif current_user.user_type == 'Instructor':
        return redirect(url_for('main.instructor.index'))
    else:
        return redirect(url_for('auth.login'))
    
