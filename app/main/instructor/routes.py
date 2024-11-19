import sys
from flask import render_template, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
import sqlalchemy as sqla
from app.main.role_validator import role_required

from app import db
from app.main.models import Section,Position
from app.main.instructor.forms import SectionForm,PositionForm

from app.main.instructor import instructor_blueprint as bp_instructor

@bp_instructor.route('/', methods=['GET'])
@bp_instructor.route('/instructor/index', methods=['GET', 'POST'])
@login_required
@role_required('Instructor')
def index():
    sections = current_user.get_sections()
        
    return render_template('instructor_index.html', title="SA Portal", sections = sections)

@bp_instructor.route('/instructor/section/create-section', methods=['GET', 'POST'])
@login_required
@role_required('Instructor')
def create_course_section():
    sform = SectionForm()
    if sform.validate_on_submit():
        new_section = Section(course_id = sform.course.data.id,
                              section_num = sform.section_num.data,
                              term = sform.term.data,
                              instructor_id = current_user.id)
        db.session.add(new_section)
        db.session.commit()
        flash('Section ' + new_section.in_course.num + '-' + new_section.section_num + ' is created')
        return redirect(url_for('main.index'))
    return render_template('register_section.html', title="Create a new section", form = sform)

@bp_instructor.route("/instructor/section/create_postitions", methods=['GET','POST'])
def create_positions():
    form = PositionForm()
    if form.validate_on_submit():
        selected_section = form.section.data
        positions = Position(
            in_section = selected_section,
            SA_num = form.SAnum.data,
            min_GPA = form.minGPA.data,
            min_grade = form.min_grade.data,
            term = form.term.data,
            instructor = current_user
        )
        db.session.add(positions)
        db.session.commit()
        flash(f'Create SA positions succesfully')
        return redirect(url_for('main.index'))
    return render_template('create_position.html', form=form)