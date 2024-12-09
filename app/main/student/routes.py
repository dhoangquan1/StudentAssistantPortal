import sys
from flask import render_template, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
import sqlalchemy as sqla
from app.main.role_validator import role_required

from app import db
from app.main.models import Section, Application, Position, Past_Enrollments
from app.main.student.forms import ApplicationForm, SortForm

from app.main.student import student_blueprint as bp_student

@bp_student.route('/', methods=['GET'])
@bp_student.route('/student/index', methods=['GET', 'POST'])
@login_required
@role_required('Student')
def index():
    positions = db.session.scalars(sqla.select(Position).where(Position.curr_SA < Position.max_SA)).all()
    
    sform = SortForm()
    if sform.validate_on_submit():
        sort_column = getattr(Position, sform.choice.data, None)
        
        if sform.prev_exp == True:
            query = db.session.query(Position).where(Position.get_prev_sa_exp()==True).order_by(sort_column.asc()) if sort_column else positions
            
        else:
            query = db.session.query(Position).order_by(sort_column.asc()) if sort_column else positions
            
        return render_template('student_index.html', title="SA Portal", positions = query, form=sform)
    
    return render_template('student_index.html', title="SA Portal", positions = positions, form=sform)
    
@bp_student.route('/student/application/<position_id>', methods=['GET', 'POST'])
@login_required
@role_required('Student')
def apply(position_id):
    position = db.session.get(Position, position_id)
    
    if position is None:
        flash('Position not found!')
        return redirect(url_for('main.student.index'))
    
    af = ApplicationForm(position_id=position_id)
    
    if af.validate_on_submit():
        new_app = Application(
            student_id = current_user.id,
            position_id = position.get_id(),
        )
        db.session.add(new_app)
        
        took_course = db.session.get(Past_Enrollments, (current_user.id, position.in_section.in_course.id))
        if took_course is None:
            new_enroll = Past_Enrollments(
                student_id = current_user.id,
                course_id = position.in_section.in_course.id,
                grade_earned = af.grade.data,
                term = "{}{}".format(af.year_took_course.data,af.term_took_course.data)
            )
            db.session.add(new_enroll)
        else:
            took_course.grade_earned = af.grade.data
            took_course.term = "{}{}".format(af.year_took_course.data,af.term_took_course.data)
        
        db.session.commit()
        flash('Applied to position')
        return redirect(url_for('main.student.index'))
    
    return render_template('application.html', form=af, position = position)