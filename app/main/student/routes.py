import sys
from flask import render_template, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
import sqlalchemy as sqla
from sqlalchemy.sql import func, case
from app.main.role_validator import role_required
from sqlalchemy import text, insert

from app import db
from app.main.models import Section, Application, Position, Past_Enrollments,Student
from app.main.student.forms import ApplicationForm, SortForm

from app.main.student import student_blueprint as bp_student

@bp_student.route('/', methods=['GET'])
@bp_student.route('/student/index', methods=['GET', 'POST'])
@login_required
@role_required('Student')
def index():
    sform = SortForm()

    qinput = {"student_id" : current_user.id}
    query = text("""
                SELECT id FROM position WHERE (position.min_GPA <= (SELECT student.gpa FROM student WHERE (student.id = :student_id)))
                AND ((SELECT past__enrollments.grade_earned FROM past__enrollments WHERE (past__enrollments.student_id = :student_id) AND (past__enrollments.course_id == (SELECT section.course_id FROM section WHERE section.id == position.section_id))) IS NULL
                OR (SELECT iif(past__enrollments.grade_earned == 'A', 3, iif(past__enrollments.grade_earned == 'B', 2, 1)) FROM past__enrollments WHERE (past__enrollments.student_id = :student_id) AND (past__enrollments.course_id == (SELECT section.course_id FROM section WHERE section.id == position.section_id))) >= position.min_grade);
    """)
    recommendID = db.session.execute(query, qinput).mappings().all()
    idlist = []
    for id in recommendID:
        idlist.append(id.id)
    recommend = db.session.query(Position).filter(Position.id.in_(idlist)).order_by(Position.min_GPA)
    query = text("""
                SELECT id FROM position WHERE ((position.min_GPA > (SELECT student.gpa FROM student WHERE (student.id = :student_id)))
                OR ((SELECT past__enrollments.grade_earned FROM past__enrollments WHERE (past__enrollments.student_id = :student_id) AND (past__enrollments.course_id == (SELECT section.course_id FROM section WHERE section.id == position.section_id))) IS NOT NULL
                AND (SELECT iif(past__enrollments.grade_earned == 'A', 3, iif(past__enrollments.grade_earned == 'B', 2, 1)) FROM past__enrollments WHERE (past__enrollments.student_id = :student_id) AND (past__enrollments.course_id == (SELECT section.course_id FROM section WHERE section.id == position.section_id))) < position.min_grade));
    """)
    wishlistID = db.session.execute(query, qinput).mappings()
    idlist = []
    for id in wishlistID:
        idlist.append(id.id)
    wishlist = db.session.query(Position).filter(Position.id.in_(idlist)).order_by(Position.min_GPA)


    if sform.validate_on_submit():
        if sform.prev_exp.data == True:

            qinput = {"student_id" : current_user.id}
            query = text("""
                        SELECT id FROM position WHERE (position.min_GPA <= (SELECT student.gpa FROM student WHERE (student.id = :student_id)))
                        AND (SELECT past__enrollments.course_id FROM past__enrollments WHERE (past__enrollments.student_id = :student_id) AND (past__enrollments.course_id == (SELECT section.course_id FROM section WHERE section.id == position.section_id))) IS NOT NULL
                        AND ((SELECT past__enrollments.grade_earned FROM past__enrollments WHERE (past__enrollments.student_id = :student_id) AND (past__enrollments.course_id == (SELECT section.course_id FROM section WHERE section.id == position.section_id))) IS NULL
                        OR (SELECT iif(past__enrollments.grade_earned == 'A', 3, iif(past__enrollments.grade_earned == 'B', 2, 1)) FROM past__enrollments WHERE (past__enrollments.student_id = :student_id) AND (past__enrollments.course_id == (SELECT section.course_id FROM section WHERE section.id == position.section_id))) >= position.min_grade);
            """)
            recommendID = db.session.execute(query, qinput).mappings().all()
            idlist = []
            for id in recommendID:
                idlist.append(id.id)
            recommend = db.session.query(Position).filter(Position.id.in_(idlist))
            query = text("""
                        SELECT id FROM position WHERE (SELECT past__enrollments.course_id FROM past__enrollments WHERE (past__enrollments.student_id = :student_id) AND (past__enrollments.course_id == (SELECT section.course_id FROM section WHERE section.id == position.section_id))) IS NOT NULL
                        AND ((position.min_GPA > (SELECT student.gpa FROM student WHERE (student.id = :student_id)))
                        OR ((SELECT past__enrollments.grade_earned FROM past__enrollments WHERE (past__enrollments.student_id = :student_id) AND (past__enrollments.course_id == (SELECT section.course_id FROM section WHERE section.id == position.section_id))) IS NOT NULL
                        AND (SELECT iif(past__enrollments.grade_earned == 'A', 3, iif(past__enrollments.grade_earned == 'B', 2, 1)) FROM past__enrollments WHERE (past__enrollments.student_id = :student_id) AND (past__enrollments.course_id == (SELECT section.course_id FROM section WHERE section.id == position.section_id))) < position.min_grade));
            """)
            wishlistID = db.session.execute(query, qinput).mappings()
            idlist = []
            for id in wishlistID:
                idlist.append(id.id)
            wishlist = db.session.query(Position).filter(Position.id.in_(idlist))

        else:
            qinput = {"student_id" : current_user.id}
            query = text("""
                        SELECT id FROM position WHERE (position.min_GPA <= (SELECT student.gpa FROM student WHERE (student.id = :student_id)))
                        AND ((SELECT past__enrollments.grade_earned FROM past__enrollments WHERE (past__enrollments.student_id = :student_id) AND (past__enrollments.course_id == (SELECT section.course_id FROM section WHERE section.id == position.section_id))) IS NULL
                        OR (SELECT iif(past__enrollments.grade_earned == 'A', 3, iif(past__enrollments.grade_earned == 'B', 2, 1)) FROM past__enrollments WHERE (past__enrollments.student_id = :student_id) AND (past__enrollments.course_id == (SELECT section.course_id FROM section WHERE section.id == position.section_id))) >= position.min_grade);
            """)
            recommendID = db.session.execute(query, qinput).mappings().all()
            idlist = []
            for id in recommendID:
                idlist.append(id.id)
            recommend = db.session.query(Position).filter(Position.id.in_(idlist))
            query = text("""
                        SELECT id FROM position WHERE ((position.min_GPA > (SELECT student.gpa FROM student WHERE (student.id = :student_id)))
                        OR ((SELECT past__enrollments.grade_earned FROM past__enrollments WHERE (past__enrollments.student_id = :student_id) AND (past__enrollments.course_id == (SELECT section.course_id FROM section WHERE section.id == position.section_id))) IS NOT NULL
                        AND (SELECT iif(past__enrollments.grade_earned == 'A', 3, iif(past__enrollments.grade_earned == 'B', 2, 1)) FROM past__enrollments WHERE (past__enrollments.student_id = :student_id) AND (past__enrollments.course_id == (SELECT section.course_id FROM section WHERE section.id == position.section_id))) < position.min_grade));
            """)
            wishlistID = db.session.execute(query, qinput).mappings()
            idlist = []
            for id in wishlistID:
                idlist.append(id.id)
            wishlist = db.session.query(Position).filter(Position.id.in_(idlist))
        if (sform.choice.data == 'min_GPA'):
            recommend = recommend.order_by(Position.min_GPA)
            wishlist = wishlist.order_by(Position.min_GPA)
        if (sform.choice.data == 'min_grade'):
            recommend = recommend.order_by(Position.min_grade)
            wishlist = wishlist.order_by(Position.min_grade)
        return render_template('student_index.html', title="SA Portal", recommend = recommend, form=sform, wishlist = wishlist)
    
    return render_template('student_index.html', title="SA Portal", recommend = recommend, form=sform, wishlist = wishlist)
    
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

@bp_student.route('/student/application/<position_id>/withdraw', methods=['GET', 'POST'])
@login_required
@role_required('Student')
def withdraw(position_id):
    if(current_user.withdraw(position_id)):
        flash('You have successfully withdrawn from the position.')
    else:
        flash('Withdrawal failed. Please try again.')
    return redirect(url_for('main.student.index'))

@bp_student.route("/student/profile", methods=['GET','POST'])
@login_required
@role_required('Student')
def view_profile():
    student = db.session.get(Student, current_user.id)
    return render_template('profile.html', student = student)

    