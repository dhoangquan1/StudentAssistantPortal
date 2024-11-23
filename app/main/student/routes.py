import sys
from flask import render_template, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
import sqlalchemy as sqla
from app.main.role_validator import role_required

from app import db
from app.main.models import Section, Application, Position
from app.main.student.forms import ApplicationForm

from app.main.student import student_blueprint as bp_student

@bp_student.route('/', methods=['GET'])
@bp_student.route('/student/index', methods=['GET', 'POST'])
@login_required
@role_required('Student')
def index():

    return render_template('student_index.html', title="SA Portal")
    
    
@bp_student.route('/student/application/<section_id>/<position_id>', methods=['GET', 'POST'])
@login_required
def apply(section_id, position_id):
    section = db.session.get(Section, section_id)
    position = db.session.get(Position, position_id)
    
    if section is None:
        flash('Section not found!')
        return redirect(url_for('main.student.index'))
    if position is None:
        flash('Position not found!')
        return redirect(url_for('main.student.index'))
    
    af = ApplicationForm()
    
    if af.validate_on_submit():
        new_app = Application(
            student_id = current_user.id,
            position_id = position.get_id(),
        )
        
        db.session.add(new_app)
        db.session.commit()
        flash('Applied to position')
        return redirect('main.student.index')
    
    return render_template('application.html', form=af)