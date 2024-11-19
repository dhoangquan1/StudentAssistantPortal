from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from app import db
from flask import  render_template,flash,redirect, request,url_for
import sqlalchemy as sqla

from app.main import main_blueprint as bp_main
from app.main.forms import PositionForm
from app.main.models import Section


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
    
@bp_main.route("/instructor/section/create_postitions", methods=['GET','POST'])
def create_positions():
    form = PositionForm()
    if form.validate_on_submit():
        selected_section = form.course_section.data
        updated_section = Section(
            instructor_id=current_user.id,  
            course_id=selected_section.in_course.id,  
            max_SA=form.SAnum.data,  
            min_GPA=form.minGPA.data, 
            section_num=selected_section.section_num,  
            term=selected_section.term,  
            min_grade=form.min_grade.data,  
            instructor=current_user  
        )
        db.session.add(updated_section)
        db.session.commit()
        flash(f'Create SA positions succesfully')
    return render_template('create_position.html', form=form)