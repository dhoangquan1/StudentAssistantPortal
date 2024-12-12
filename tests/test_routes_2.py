from datetime import datetime
import os
import pytest
from flask import  url_for 
from app import create_app, db
from app.main.models import Course, Student, Past_Enrollments,Instructor,Section,Position, Application
from config import Config
import sqlalchemy as sqla

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'you-will-never-guess'
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True

@pytest.fixture(scope='module')
def test_client():
    # create the flask application ; configure the app for tests
    flask_app = create_app(config_class=TestConfig)

    # db.init_app(flask_app)
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
    ctx = flask_app.test_request_context()
    ctx.push()

    yield  testing_client 
    # this is where the testing happens!

    ctx.pop()
    
def new_student( email, first_name, last_name, wpi_id, phone, passwd, major=None, gpa=None, grad_date=None, prev_enrolled=None):
    student = Student(
        email=email,
        first_name=first_name,
        last_name=last_name,
        wpi_id=wpi_id,
        phone=phone,
        major=major,
        gpa=gpa,
        grad_date=grad_date,
    )
    student.set_password(passwd) 
    # if prev_enrolled:
    #     for enrollment in prev_enrolled:
    #         course = Course.query.get(enrollment.get('course_id'))  # Use query to mock course retrieval
    #         if course:
    #             past_enrollment = Past_Enrollments(
    #                 student_id=None,  
    #                 course_id=course.id,
    #                 grade_earned=enrollment.get('grade_earned'),
    #                 sa_before=enrollment.get('sa_before', False),
    #                 term=enrollment.get('term')
    #             )
    #             student.prev_enrolled.append(past_enrollment)
    for course_id, grade, sa_before, term in prev_enrolled:
        enrollment = Past_Enrollments(
            student_id=student.id,
            course_id=course_id,
            grade_earned=grade,
            sa_before=sa_before,
            term=term,
        )
        db.session.add(enrollment)
        
    return student

def new_instructor( email, first_name, last_name, wpi_id, phone, passwd, sections=None):
    instructor = Instructor(
        email=email,
        first_name=first_name,
        last_name=last_name,
        wpi_id=wpi_id,
        phone=phone,
    )
    instructor.set_password(passwd)

    return instructor


@pytest.fixture
def init_database(request,test_client):
    # Create the database and the database table
    db.create_all()
    # initialize the course
    courses = [{'num':'CS1101','title':'Introduction To Program Design'},
            {'num':'CS2022','title':'Discrete Mathematics'},
            {'num':'CS2223','title':'Algorithms'},
            {'num':'CS3013','title':'Operating Systems'}, 
            {'num':'CS3431','title': 'Database Systems I'}]
    for c in courses:
            db.session.add(Course(num = c['num'], title = c['title']))    
    db.session.commit()
    #add a user    
    student1 = new_student(
        'john@wpi.edu', 
        'John', 
        'John', 
        '123123123', 
        '123-456-7890', 
        '123', 
        'Computer Science', 
        3.75, 
        datetime(2025, 5, 20),  
        []  
    )
    db.session.add(student1)
    db.session.commit()     

    instructor1 = new_instructor(
        'sakire@wpi.edu', 
        'Sakire', 
        'Sakire', 
        '321321321', 
        '133-456-7890', 
        '123', 
    )
    db.session.add(instructor1)

    course = db.session.scalars(sqla.select(Course).where(Course.num == 'CS1101')).first()
    section1 = Section(course_id = course.id, section_num =  '01', term = "2025B", instructor_id = instructor1.id)
    
    course = db.session.scalars(sqla.select(Course).where(Course.num == 'CS2022')).first()
    section2 = Section(course_id = course.id, section_num =  '01', term = "2025A", instructor_id = instructor1.id)
    
    db.session.add(section1) 
    db.session.add(section2) 
    db.session.commit()

    # Add a position for the section
    position1 = Position(
        section_id=section1.id,
        min_GPA=3.0,
        min_grade='B',
        prev_sa_exp=False,
        max_SA=3
    )

    position2 = Position(
        section_id=section2.id,
        min_GPA=2.0,
        min_grade='C',
        prev_sa_exp=True,
        max_SA=2
    )

    db.session.add(position1)
    db.session.add(position2)
    db.session.commit()

    # Add an application for the student
    application1 = Application(
        student_id=student1.id,
        position_id=position1.id,
        status='Pending'
    )
    db.session.add(application1)
    
    
    
    db.session.commit()    
    
    yield  

    db.drop_all()

def do_login(test_client, path , email, passwd):
    response = test_client.post(path, 
                          data=dict(email= email, password=passwd, remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    
def do_logout(test_client, path):
    response = test_client.get(path,                       
                          follow_redirects = True)
    assert response.status_code == 200

def test_student_page(request,test_client,init_database):
    do_login(test_client, path = '/login', email = 'john@wpi.edu', passwd = '123')
    response = test_client.get('/student/index')
    assert response.status_code == 200
    assert b'Welcome to Student Assistant Portal!' in response.data
    assert b"CS1101-01 : Introduction To Program Design" in response.data
    assert b"CS2022-01 : Discrete Mathematics" in response.data
    assert b"Instructor: Sakire Sakire" in response.data
    do_logout(test_client, path = '/logout')

def test_application_page(request, test_client, init_database):
    do_login(test_client, path = '/login', email = 'john@wpi.edu', passwd = '123')
    course = db.session.scalars(sqla.select(Course).where(Course.num == 'CS2022')).first()
    section = db.session.scalars(sqla.select(Section).where(Section.course_id == course.id).where(Section.term == '2025A').where(Section.section_num == '01')).first()
    position = db.session.scalars(sqla.select(Position).where(Position.section_id == section.id).where(Position.min_GPA == 2.0)).first()
    response = test_client.get(f'/student/application/{position.id}')
    assert response.status_code == 200
    assert b"Applying to" in response.data
    assert b"Instructor: Sakire Sakire" in response.data
    do_logout(test_client, path = '/logout')

def test_applying(test_client, init_database):
    do_login(test_client, path = '/login', email = 'john@wpi.edu', passwd = '123')
    course = db.session.scalars(sqla.select(Course).where(Course.num == 'CS2022')).first()
    section = db.session.scalars(sqla.select(Section).where(Section.course_id == course.id).where(Section.term == '2025A').where(Section.section_num == '01')).first()
    position = db.session.scalars(sqla.select(Position).where(Position.section_id == section.id).where(Position.min_GPA == 2.0)).first()
    response = test_client.post(
        f'/student/application/{position.id}',
        data=dict(
            grade = 'A',
            year_took_course = '2024',
            term_took_course = 'A',
        ),follow_redirects = True
    )
    assert response.status_code == 200
    assert b"Already Applied!" in response.data
    do_logout(test_client, path = '/logout')

def test_SA_applications(test_client, init_database):
    do_login(test_client, path = '/login', email = 'sakire@wpi.edu', passwd = '123')
    response = test_client.get('/instructor/index')
    assert response.status_code == 200
    assert b"Welcome to Student Assistant Portal!"
    assert b"John John"

    