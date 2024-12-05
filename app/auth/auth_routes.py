
from datetime import datetime, timezone
from flask import render_template, flash, redirect, url_for, request, session
from flask_login import login_user, current_user, logout_user, login_required
import identity.web

from app import db
from app.auth import auth_blueprint as bp_auth 
import sqlalchemy as sqla
from config import Config as app_config

from app.auth.auth_forms import InstructorRegistrationForm, StudentRegistrationForm, LoginForm, RoleForm
from app.main.models import User, Instructor, Student, Past_Enrollments

ssoauth = identity.web.Auth(
    session=session,
    authority=app_config.AUTHORITY,
    client_id=app_config.CLIENT_ID,
    client_credential=app_config.CLIENT_SECRET,
)

@bp_auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    rform = RoleForm()

    if rform.validate_on_submit():

        if rform.role.data == 'Instructor':
            return redirect(url_for('auth.register_instructor'))
        if rform.role.data == 'Student':
            return redirect(url_for('auth.register_student'))
    
    return render_template('register.html', title="Register", form = rform)

@bp_auth.route('/instructor/register', methods=['GET', 'POST'])
def register_instructor():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    rform = InstructorRegistrationForm()
    rform.phone_code.choices = InstructorRegistrationForm.show_phone_codes()
    if rform.validate_on_submit():
        new_user = Instructor(
            first_name = rform.first_name.data,
            last_name = rform.last_name.data,
            email = rform.email.data,
            wpi_id = rform.wpi_id.data,
            phone = rform.phone_code.data + rform.phone.data,
            user_type = 'Instructor')
        
        new_user.set_password(rform.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.index'))
    return render_template('register_instructor.html', title="Register", form = rform)

@bp_auth.route('/student/register', methods=['GET', 'POST'])
def register_student():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    rform = StudentRegistrationForm()
    rform.phone_code.choices = StudentRegistrationForm.show_phone_codes()
    if rform.validate_on_submit():
        new_user = Student(
            first_name = rform.first_name.data,
            last_name = rform.last_name.data,
            email = rform.email.data,
            wpi_id = rform.wpi_id.data,
            phone = rform.phone_code.data + rform.phone.data,
            major = rform.major.data,
            gpa = float(rform.gpa.data),
            grad_date = rform.grad_date.data,
            user_type = 'Student')  
        
        new_user.set_password(rform.password.data)
        db.session.add(new_user)
        
        for c in rform.sa_courses.data:
            enrollment = Past_Enrollments(course_id = c.id, sa_before=True)
            new_user.prev_enrolled.add(enrollment)
            
        db.session.commit()
        
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.index'))
    return render_template('register_student.html', title="Register", form = rform)

@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    lform = LoginForm()
    if lform.validate_on_submit():
        query = sqla.select(User).where(User.email == lform.email.data)
        user = db.session.scalars(query).first()
        if (user is None) or (user.check_password(lform.password.data) == False):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=lform.remember_me.data)
        flash('The user {} has successfully logged in!'.format(current_user.email))
        return redirect(url_for('main.index'))
    return render_template('login.html', form = lform)

@bp_auth.route("/loginsso")
def loginsso():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    return render_template("sso.html", **ssoauth.log_in(
        scopes=app_config.SCOPE, # Have user consent to scopes during log-in
        redirect_uri=url_for("auth.auth_response", _external=True), # Optional. If present, this absolute URL must match your app's redirect_uri registered in Microsoft Entra admin center
        prompt="select_account",  # Optional.
        ))

@bp_auth.route(app_config.REDIRECT_PATH)
def auth_response():
    result = ssoauth.complete_log_in(request.args)
    if "error" in result:
        flash('Something went wrong with SSO {}'.format(result.get('error')))
        return redirect(url_for('auth.login'))
    else:
        query = sqla.select(User).where(User.email == ssoauth.get_user()["preferred_username"])
        user = db.session.scalars(query).first()
        if (user is None):
            flash('User does not exist! Please register a new user.')
            return redirect(url_for('auth.register'))
        login_user(user, remember=False)
        session['ssologin'] = ssoauth.get_user()["preferred_username"]
        flash('The user {} has successfully logged in with SSO!'.format(current_user.email))
    return redirect(url_for('main.index'))

@bp_auth.route('/logout', methods=['GET'])
@login_required
def logout():
    if session.get('ssologin'):
        ssoauth.log_out(url_for("main.index", _external=True))
    logout_user()
    return redirect(url_for('main.index'))