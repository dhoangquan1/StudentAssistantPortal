from datetime import datetime
import os
import pytest
from flask import  url_for 
from app import create_app, db
from app.main.models import Course, Student, Past_Enrollments,Instructor,Section,Position
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
    db.session.add(section1)
    db.session.commit()     

    yield  

    db.drop_all()
        


def test_register_page(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/student/register' page is requested (GET)
    THEN check that the response is valid
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.get('/student/register')
    assert response.status_code == 200
    assert b"Register" in response.data
    
    response = test_client.get('/instructor/register')
    assert response.status_code == 200
    assert b"Register" in response.data

    
def test_register_student(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/student/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.post(
        '/student/register',
        data=dict(
            email='jin@wpi.edu',
            password="123",
            password2="123",
            first_name='Jin',
            last_name='Ash',
            wpi_id='312456789',
            phone='506-333-8888',
            phone_code='1',
            major='Computer Science',
            gpa=3.7,
            grad_date='2025-05-15',
            sa_courses=[],
        ),
        follow_redirects=True
    )
    assert response.status_code == 200
    s = db.session.scalars(sqla.select(Student).where(Student.email == 'jin@wpi.edu')).first()
    s_count = db.session.scalar(sqla.select(db.func.count()).where(Student.email == 'jin@wpi.edu'))

    assert s.first_name == 'Jin'
    assert s_count == 1
    assert b'Congratulations, you are now a registered user!' in response.data 
    assert b'Please log in to access this page.' in response.data  
    
def test_register_instructor(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/instructor/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.post(
        '/instructor/register',
        data=dict(
            email='star@wpi.edu',
            password="123",
            password2="123",
            first_name='Star',
            last_name='Bob',
            phone_code='1',
            wpi_id='312656789',
            phone='506-333-0808'
        ),follow_redirects = True)
    assert response.status_code == 200
    i = db.session.scalars(sqla.select(Instructor).where(Instructor.email == 'star@wpi.edu')).first()
    i_count = db.session.scalar(sqla.select(db.func.count()).where(Instructor.email == 'star@wpi.edu'))

    assert i.first_name == 'Star'
    assert i_count == 1
    assert b'Congratulations, you are now a registered user!' in response.data 
    assert b'Please log in to access this page.' in response.data  



def test_invalidlogin(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with wrong credentials
    THEN check that the response is valid and login is refused 
    """
    response = test_client.post('/login', 
                          data=dict(email='john@wpi.edu', password='321',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data

    response = test_client.post('/login', 
                          data=dict(email='sakire@wpi.edu', password='231',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data


    
def do_login(test_client, path , email, passwd):
    response = test_client.post(path, 
                          data=dict(email= email, password=passwd, remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    
def do_logout(test_client, path):
    response = test_client.get(path,                       
                          follow_redirects = True)
    assert response.status_code == 200

def test_login_logout(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/student/login' form is submitted (POST) with correct credentials
    THEN check that the response is valid and login is succesfull 
    """
    do_login(test_client, path = '/login', email = 'sakire@wpi.edu', passwd = '123')
    do_login(test_client, path = '/login', email = 'john@wpi.edu', passwd = '123')
    do_logout(test_client, path = '/logout')

    
def test_create_section(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing , after user logs in,
    WHEN the '/course/create' page is requested (GET)  AND '/course/create' form is submitted (POST)
    THEN check that response is valid and the class is successfully created in the database
    """
    #first login
    do_login(test_client, path = '/login', email = 'sakire@wpi.edu', passwd = '123')
    
    response = test_client.get('/instructor/section')
    assert response.status_code == 200
    assert b"Create a new section" in response.data  
    course = db.session.scalars(sqla.select(Course).where(Course.num == 'CS1101')).first()    
    response = test_client.post(
        '/instructor/section',
        data=dict(
            course=str(course.id), 
            section_num='02',
            term='2025B',
        ),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Section CS1101-02 is created' in response.data
    

    s = db.session.scalars(sqla.select(Section).where(Section.course_id == course.id)).first()
    s_count = db.session.scalar(sqla.select(db.func.count()).where(Section.course_id == course.id))
    assert s.in_course.title == 'Introduction To Program Design'  
    assert s_count == 2

    do_logout(test_client, path = '/logout')

    
def test_create_position(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing , after user logs in,
    WHEN the '/instructor/position' page is requested (GET)  AND '/instructor/position' form is submitted (POST)
    THEN check that response is valid and the class is successfully created in the database
    """
    #first login
    do_login(test_client, path = '/login', email = 'sakire@wpi.edu', passwd = '123')
    
    response = test_client.get('/instructor/position')
    assert response.status_code == 200
    assert b"Create a New SA Position" in response.data  
    section =  db.session.scalars(sqla.select(Section).where(Section.section_num == '01')).first()
    response = test_client.post(
    '/instructor/position',
    data=dict(
        section=str(section.id),  
        SAnum = 2,
        minGPA = 2,
        min_grade = 3,
        prev_sa_exp = True,
    ),
    follow_redirects=True
)
    assert response.status_code == 200
    assert b'Create SA positions successfully' in response.data

    p = db.session.scalars(sqla.select(Position).where(Position.section_id == section.id)).first()
    p_count = db.session.scalar(sqla.select(db.func.count()).where(Position.section_id == section.id))
    assert p.max_SA == 2  
    assert p.in_section.term == '2025B'
    assert p_count == 1

    do_logout(test_client, path = '/logout')
    
