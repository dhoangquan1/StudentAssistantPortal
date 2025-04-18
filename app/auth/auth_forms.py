from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, FloatField, DateField, RadioField, SelectMultipleField
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Email, Length, NumberRange
from wtforms.widgets import ListWidget, CheckboxInput

import datetime
import phonenumbers
from phonenumbers import PhoneMetadata

from app import db
from app.main.models import User, Course
import sqlalchemy as sqla


class RoleForm(FlaskForm):
    role = RadioField('Choose your account role',choices = [('Student', 'Student'), ('Instructor', 'Instructor')], default='Student')
    submit = SubmitField('Register')

class RegistrationForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()] )
    wpi_id = StringField('WPI ID', validators=[DataRequired(), Length(min=9, max=9)])
    phone_code = SelectField('Country Code', 
                                        choices=None)
    phone = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
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
        
    @staticmethod
    def show_phone_codes():
        all_regions = phonenumbers.SUPPORTED_REGIONS  # Get all supported regions
        phone_codes = []
        for region in sorted(all_regions):
            metadata = PhoneMetadata.metadata_for_region(region)
            country_name = region  
            country_code = metadata.country_code  
            phone_codes.append((country_code, f"{country_name} (+{country_code})"))
        return phone_codes
    
    def validate_phone(self, phone):
        phone_code = self.phone_code.data
        if len(phone.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(f"+{phone_code}{phone.data}")
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number. use something else')
        except:
            raise ValidationError(f'Invalid phone number. +{phone_code}{phone.data}')

class InstructorRegistrationForm(RegistrationForm):
    placeholder = StringField('placeholder')
    
    
class StudentRegistrationForm(RegistrationForm):
    major = StringField('Major', validators=[DataRequired()])
    gpa = FloatField('Cumulative GPA', validators=[DataRequired(), NumberRange(max=4)])
    grad_date = DateField('Expected Graduation Date', validators=[DataRequired()])
    sa_courses = QuerySelectMultipleField('Previous Student Assistant Courses',
                                            query_factory = lambda : db.session.scalars(sqla.select(Course)),
                                            get_label= lambda course: course.title,
                                            widget = ListWidget(prefix_label=False),
                                            option_widget = CheckboxInput())

    def validate_grad_date(self, grad_date):
        if grad_date.data <= datetime.date.today():
            raise ValidationError('Invalid graduation date.')
    

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In')