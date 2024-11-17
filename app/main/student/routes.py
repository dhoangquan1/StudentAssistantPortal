import sys
from flask import render_template, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
import sqlalchemy as sqla
from app.main.role_validator import role_required

from app import db
# from app.main.models import Post, Tag, postTags
# from app.main.student.forms import PostForm, SortForm

from app.main.student import student_blueprint as bp_student

@bp_student.route('/', methods=['GET'])
@bp_student.route('/student/index', methods=['GET', 'POST'])
@role_required('Student')
@login_required
def index():

    return render_template('student_index.html', title="SA Portal")
    