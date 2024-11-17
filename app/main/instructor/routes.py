import sys
from flask import render_template, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
import sqlalchemy as sqla
from app.main.role_validator import role_required

from app import db

from app.main.instructor import instructor_blueprint as bp_instructor

@bp_instructor.route('/', methods=['GET'])
@bp_instructor.route('/instructor/index', methods=['GET', 'POST'])
@role_required('Instructor')
@login_required
def index():
   
        
    return render_template('instructor_index.html', title="SA Portal")
