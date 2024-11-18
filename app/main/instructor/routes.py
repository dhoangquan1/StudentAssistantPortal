import sys
from flask import render_template, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
import sqlalchemy as sqla
from app.main.role_validator import role_required

from app import db
from app.main.models import Section
from app.main.instructor.forms import SectionForm

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
