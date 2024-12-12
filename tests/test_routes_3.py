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
    db.session.add(section1) 
    db.session.commit()

    # Add a position for the section
    position1 = Position(
        section_id=section1.id,
        min_GPA=3.0,
        min_grade='B',
        prev_sa_exp=False,
        max_SA=3
    )
    db.session.add(position1)
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
    
def do_login(test_client, path , email, passwd):
    response = test_client.post(path, 
                        data=dict(email= email, password=passwd, remember_me=False),
                        follow_redirects = True)
    assert response.status_code == 200
    
def do_logout(test_client, path):
    response = test_client.get(path,                       
                        follow_redirects = True)
    assert response.status_code == 200

def test_student_profile(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the ApplicationForm in '/student/application/<position_id>' is submitted (POST) AND the '/student/profile' page is requested (GET) 
    THEN check that the response is valid
    """
    
    do_login(test_client, path = '/login', email = 'john@wpi.edu', passwd = '123')
    
    position_id = db.session.scalars(sqla.select(Position)).first().id
    response = test_client.post(
        f'/student/application/{position_id}',
        data={'position_id': position_id},
        follow_redirects=True
    )
    positions = db.session.scalars(sqla.select(Student).where(Student.email == "john@wpi.edu")).first().get_all_applications()
    # Feedback after applying
    assert response.status_code == 200
    assert b"Applied to position"
    assert len(positions) == 1
    
    response = test_client.get('/student/profile')
    assert response.status_code == 200
    assert b"Profile" in response.data
    # Feedback for showing pending applications
    assert b"Pending" in response.data
    # Feedback for showing withdrawn button
    assert b"Withdraw" in response.data
    
    response2 = test_client.post(
        f'/student/application/{position_id}/withdraw',
        data={'position_id': position_id},
        follow_redirects=True
    )
    assert response2.status_code == 200
    assert b"You have successfully withdrawn" in response2.data
    
    positions_after = db.session.scalars(sqla.select(Student).where(Student.email == "john@wpi.edu")).first().get_all_applications()
    assert len(positions_after) == 0
    
    do_logout(test_client, path='/logout')

    
def test_instructor_view(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/instructor/student/<student_id>/profile' page is requested (GET)
    AND the '/instructor/position/<position_id>/<student_id>' page is requested (POST)
    THEN check that the response is valid
    """
    do_login(test_client, path = '/login', email = 'sakire@wpi.edu', passwd = '123')
    
    with test_client.application.app_context():
        # Ensure current_user is available
        from flask_login import current_user
        
        student = db.session.scalars(sqla.select(Student).where(Student.email == 'john@wpi.edu')).first()
        assert student is not None, "Student should exist in the database"
        
        student_id = student.id

        position = db.session.scalars(sqla.select(Position)).first()
        assert position is not None, "Position should exist in the database"

        position_id = position.id

        # Perform the POST request to update the student's profile
        response = test_client.get(
            f'/instructor/student/{student_id}/profile',
            data={'position_id': position_id},
            follow_redirects=True
        )

        # Verify the response status code
        assert response.status_code == 200

        # Query the database to check updates
        updated_application = db.session.scalars(
            sqla.select(Application).where(Application.student_id == student_id, Application.position_id == position_id)
        ).first()

        assert updated_application is not None
        assert updated_application.status == 'Pending'

        # Verify the student's name in the result
        assert student.first_name == 'John'
        assert student.last_name == 'John'
        
        assert b"Student Profile" in response.data 
        assert b"Course" in response.data
        
        response2 = test_client.post(
            f'/instructor/position/{position_id}/{student_id}',
            data={'student_id': student_id, 'position_id': position_id},
            follow_redirects=True
        )
        
        position = db.session.get(Position, position_id)
        
        assert position.curr_SA == 1
        assert b"Dashboard" in response2.data
        
    do_logout(test_client, path='/logout')
