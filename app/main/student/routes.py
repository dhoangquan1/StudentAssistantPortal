import sys
from flask import render_template, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
import sqlalchemy as sqla
from app.main.role_validator import role_required

from app import db
from app.main.models import Position


from app.main.student import student_blueprint as bp_student

@bp_student.route('/', methods=['GET'])
@bp_student.route('/student/index', methods=['GET', 'POST'])
@login_required
@role_required('Student')
def index():
    positions = db.session.scalars(sqla.select(Position).where(Position.curr_SA < Position.max_SA))
    return render_template('student_index.html', title="SA Portal", positions = positions)
    
@bp_student.route('/student/application/<position_id>', methods=['GET', 'POST'])
@login_required
@role_required('Student')
def apply(position_id):

    return render_template('apply_position.html', title="SA Portal")
    