import sys
from flask import render_template, flash, redirect, request, url_for, jsonify
from flask_login import login_required, current_user
import sqlalchemy as sqla
from app.main.role_validator import role_required

from app import db
from app.main.models import Section,Position, Student,Application
from app.main.instructor.forms import SectionForm,PositionForm

from app.main.instructor import instructor_blueprint as bp_instructor

@bp_instructor.route('/instructor', methods=['GET'])
@bp_instructor.route('/instructor/index', methods=['GET', 'POST'])
@login_required
@role_required('Instructor')
def index():
    sections = current_user.get_sections()
    positions = current_user.get_positions()
    return render_template('instructor_index.html', title="SA Portal", sections = sections, positions = positions)

@bp_instructor.route('/instructor/section', methods=['GET', 'POST'])
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

@bp_instructor.route("/instructor/position", methods=['GET','POST'])
@login_required
@role_required('Instructor')
def create_positions():
    form = PositionForm()
    if form.validate_on_submit():
        positions = Position(
            section_id = form.section.data.id,
            max_SA = form.SAnum.data,
            min_GPA = form.minGPA.data,
            min_grade = form.min_grade.data,
            prev_sa_exp = form.prev_sa_exp.data,
        )
        db.session.add(positions)
        db.session.commit()
        flash(f'Create SA positions succesfully')
        return redirect(url_for('main.index'))
    return render_template('create_position.html', form=form)

@bp_instructor.route("/instructor/student/<student_id>/profile", methods=['GET','POST'])
@login_required
@role_required('Instructor')
def view_profile(student_id):
    student = db.session.get(Student, student_id)
    return render_template('student_profile.html', student = student)




@bp_instructor.route("/instructor/<int:position_id>/assign/<int:student_id>", methods=['GET'])
@login_required
@role_required('Instructor')
def assign(position_id, student_id):
    position = db.session.get(Position, position_id)
    application = db.session.query(Application).filter_by(student_id=student_id, position_id=position_id).first()
    if position.curr_SA >= position.max_SA:
        flash("Position is already fully assigned.", "warning")
        return redirect(url_for('main.index'))
    application.status = 'Assigned'
    application.applicant.sa_pos_id = position_id
    position.curr_SA += 1
    db.session.commit()
    return redirect(url_for('main.index'))


    