from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, FloatField, DateField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Email, Length, NumberRange
from wtforms.widgets import ListWidget, CheckboxInput

from app import db
from app.main.models import User, Course
import sqlalchemy as sqla


class RoleForm(FlaskForm):
    role = SelectField('Choose your role',choices = [('Student', 'Student'), ('Instructor', 'Instructor')])
    submit = SubmitField('Register')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()] )
    wpi_id = StringField('WPI ID', validators=[DataRequired(), Length(min=9, max=9)])
    phone = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Account Role',choices = [('Student', 'Student'), ('Instructor', 'Instructor')])   
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        query = sqla.select(User).where(User.username == username.data)
        user = db.session.scalars(query).first()
        if user is not None:
            raise ValidationError('The username already exists! Please use a different username.')
    
    def validate_email(self, email):
        query = sqla.select(User).where(User.email == email.data)
        user = db.session.scalars(query).first()
        if user is not None:
            raise ValidationError('The email already exists! Please use a different email.')
        
    def validate_wpi_id(self, wpi_id):
        query = sqla.select(User).where(User.wpi_id == wpi_id.data)
        user = db.session.scalars(query).first()
        if user is not None:
            raise ValidationError('The ID is associated with another account! Please log in to your account.')

class InstructorRegistrationForm(RegistrationForm):
    placeholder = StringField('placeholder', validators=[DataRequired()])
    
    
class StudentRegistrationForm(RegistrationForm):
    major = StringField('Major', validators=[DataRequired()])
    gpa = FloatField('GPA', validators=[DataRequired(), NumberRange(max=4)])
    grad_date = DateField('Graduation Date', validators=[DataRequired()])
    sa_courses = QuerySelectMultipleField('Previous Student Assistant Courses',
                                            query_factory = lambda : db.session.scalars(sqla.select(Course)),
                                            get_label= lambda course: course.title,
                                            widget = ListWidget(prefix_label=False),
                                            option_widget = CheckboxInput())


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In')