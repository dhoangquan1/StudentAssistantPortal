import warnings
warnings.filterwarnings("ignore")

from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.main.models import User, Student, Instructor, Course, Section, Position, Past_Enrollments, Application
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    
class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = Instructor(email='quan@wpi.edu',
                       first_name='Quan',
                       last_name='Dinh',
                       wpi_id='123456789',
                       phone='123456789',
                       user_type = 'Instructor')
        u.set_password('123')
        
        self.assertFalse(u.check_password('456'))
        self.assertTrue(u.check_password('123'))

    def test_add_section_1(self):
        u1 = Instructor(email='quan@wpi.edu',
                       first_name='Quan',
                       last_name='Dinh',
                       wpi_id='123456789',
                       phone='123456789',
                       user_type = 'Instructor')
        db.session.add(u1)
        db.session.commit()
        c1 = Course(num='CS3733', title="Soft Eng")
        db.session.add(c1)
        db.session.commit()
        self.assertEqual(len(u1.get_sections()), 0)
        s1 = Section(instructor_id=u1.id, course_id=c1.id, section_num='01', term ='2024C')
        db.session.add(s1)
        db.session.commit()
        
        self.assertEqual(len(u1.get_sections()), 1)
        self.assertEqual(u1.get_sections()[0].in_course.num, 'CS3733')
        self.assertEqual(u1.get_sections()[0].in_course.title, 'Soft Eng')
        self.assertEqual(u1.get_sections()[0].section_num, '01')
        self.assertEqual(u1.get_sections()[0].term, '2024C')
            
    def test_add_section_2(self):
        u1 = Instructor(email='quan@wpi.edu',
                       first_name='Quan',
                       last_name='Dinh',
                       wpi_id='123456789',
                       phone='123456789',
                       user_type = 'Instructor')
        u2 = Instructor(email='christine@wpi.edu',
                       first_name='Christine',
                       last_name='Mae',
                       wpi_id='987654321',
                       phone='9876654321',
                       user_type = 'Instructor')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        c1 = Course(num='CS3733', title="Soft Eng")
        c2 = Course(num='CS2223', title="Algorithms")
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()
        self.assertEqual(len(u1.get_sections()), 0)
        self.assertEqual(len(u2.get_sections()), 0)
        s1 = Section(instructor_id=u1.id, course_id=c1.id, section_num='01', term ='2024C')
        s2 = Section(instructor_id=u1.id, course_id=c2.id, section_num='02', term ='2024B')
        s3 = Section(instructor_id=u2.id, course_id=c1.id, section_num='02', term ='2024B')
        db.session.add(s1)
        db.session.add(s2)
        db.session.add(s3)
        db.session.commit()
        
        # test the sections of the first user
        self.assertEqual(len(u1.get_sections()), 2)
        self.assertEqual(u1.get_sections()[1].in_course.num, 'CS2223')
        self.assertEqual(u1.get_sections()[1].in_course.title, 'Algorithms')
        self.assertEqual(u1.get_sections()[1].section_num, '02')
        self.assertEqual(u1.get_sections()[1].term, '2024B')
        
        # test the sections of the second user
        self.assertEqual(len(u2.get_sections()), 1)
        self.assertEqual(u2.get_sections()[0].in_course.num, 'CS3733')
        self.assertEqual(u2.get_sections()[0].in_course.title, 'Soft Eng')
        self.assertEqual(u2.get_sections()[0].section_num, '02')
        self.assertEqual(u2.get_sections()[0].term, '2024B')
        
    def test_add_position_1(self):
        u1 = Instructor(email='quan@wpi.edu',
                       first_name='Quan',
                       last_name='Dinh',
                       wpi_id='123456789',
                       phone='123456789',
                       user_type = 'Instructor')
        db.session.add(u1)
        db.session.commit()
        c1 = Course(num='CS3733', title="Soft Eng")
        db.session.add(c1)
        db.session.commit()
        self.assertEqual(len(u1.get_sections()), 0)
        s1 = Section(instructor_id=u1.id, course_id=c1.id, section_num='01', term ='2024C')
        db.session.add(s1)
        db.session.commit()
        p1 = Position(section_id=s1.id, min_GPA=4, prev_sa_exp=False, max_SA=2)
        db.session.add(p1)
        db.session.commit()
        
        self.assertEqual(len(u1.get_positions()), 1)
        self.assertEqual(u1.get_positions()[0].in_section.section_num, '01')
        self.assertEqual(u1.get_positions()[0].in_section.term, '2024C')
        self.assertEqual(u1.get_positions()[0].max_SA, 2)
        self.assertEqual(u1.get_positions()[0].min_GPA, 4)
        self.assertEqual(u1.get_positions()[0].prev_sa_exp, False)
        
    def test_add_position_2(self):
        u1 = Instructor(email='quan@wpi.edu',
                       first_name='Quan',
                       last_name='Dinh',
                       wpi_id='123456789',
                       phone='123456789',
                       user_type = 'Instructor')
        u2 = Instructor(email='christine@wpi.edu',
                       first_name='Christine',
                       last_name='Mae',
                       wpi_id='987654321',
                       phone='9876654321',
                       user_type = 'Instructor')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        c1 = Course(num='CS3733', title="Soft Eng")
        c2 = Course(num='CS2223', title="Algorithms")
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()
        self.assertEqual(len(u1.get_sections()), 0)
        self.assertEqual(len(u2.get_sections()), 0)
        s1 = Section(instructor_id=u1.id, course_id=c1.id, section_num='01', term ='2024C')
        s2 = Section(instructor_id=u2.id, course_id=c1.id, section_num='02', term ='2024B')
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()
        p1 = Position(section_id=s1.id, min_GPA=4, prev_sa_exp=False, max_SA=2)
        p2 = Position(section_id=s1.id, min_GPA=3, prev_sa_exp=True, max_SA=3)
        p3 = Position(section_id=s2.id, min_GPA=4, prev_sa_exp=False, max_SA=2)
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.commit()
        
        self.assertEqual(len(u1.get_positions()), 2)
        self.assertEqual(u1.get_positions()[1].in_section.section_num, '01')
        self.assertEqual(u1.get_positions()[1].in_section.term, '2024C')
        self.assertEqual(u1.get_positions()[1].max_SA, 3)
        self.assertEqual(u1.get_positions()[1].min_GPA, 3)
        self.assertEqual(u1.get_positions()[1].prev_sa_exp, True)
        
        self.assertEqual(len(u2.get_positions()), 1)
        self.assertEqual(u2.get_positions()[0].in_section.section_num, '02')
        self.assertEqual(u2.get_positions()[0].in_section.term, '2024B')
        self.assertEqual(u2.get_positions()[0].max_SA, 2)
        self.assertEqual(u2.get_positions()[0].min_GPA, 4)
        self.assertEqual(u2.get_positions()[0].prev_sa_exp, False)

    def test_add_student_data(self):
        u1 = Student(email='quan@wpi.edu',
                       first_name='Quan',
                       last_name='Dinh',
                       wpi_id='123456789',
                       phone='123456789',
                       user_type = 'Student',
                       major='CS',
                       gpa=4,
                       grad_date=datetime.now())
        db.session.add(u1)
        db.session.commit()
        
        self.assertEqual(u1.major, 'CS')
        self.assertEqual(u1.gpa, 4)
        self.assertEqual(u1.sa_pos_id, None)

    def test_past_enrollments_1(self):
        u1 = Student(email='quan@wpi.edu',
                       first_name='Quan',
                       last_name='Dinh',
                       wpi_id='123456789',
                       phone='123456789',
                       user_type = 'Student',
                       major='CS',
                       gpa=4,
                       grad_date=datetime.now())
        db.session.add(u1)
        db.session.commit()
        c1 = Course(num='CS3733', title="Soft Eng")
        c2 = Course(num='CS2223', title="Algorithms")
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()
        self.assertEqual(len(u1.get_prev_enrolled()), 0)
        pe1 = Past_Enrollments(student_id=u1.id, course_id=c1.id, sa_before=True)
        pe2 = Past_Enrollments(student_id=u1.id, course_id=c2.id, grade_earned='B', sa_before=False, term='2023C')
        db.session.add(pe1)
        db.session.add(pe2)
        db.session.commit()
        
        self.assertEqual(len(u1.get_prev_enrolled()), 2)
        self.assertEqual(u1.get_prev_enrolled()[1].course.num, 'CS2223')
        self.assertEqual(u1.get_prev_enrolled()[1].course.title, 'Algorithms')
        self.assertEqual(u1.get_prev_enrolled()[1].grade_earned, 'B')
        self.assertEqual(u1.get_prev_enrolled()[1].sa_before, False)
        self.assertEqual(u1.get_prev_enrolled()[1].term, '2023C')

    def test_past_enrollments_2(self):
        u1 = Student(email='quan@wpi.edu',
                       first_name='Quan',
                       last_name='Dinh',
                       wpi_id='123456789',
                       phone='123456789',
                       user_type = 'Student',
                       major='CS',
                       gpa=4,
                       grad_date=datetime.now())
        u2 = Student(email='christine@wpi.edu',
                       first_name='Christine',
                       last_name='Mae',
                       wpi_id='987654321',
                       phone='9876654321',
                       user_type = 'Student',
                       major='DS',
                       gpa=3.5,
                       grad_date=datetime.now())
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        c1 = Course(num='CS3733', title="Soft Eng")
        c2 = Course(num='CS2223', title="Algorithms")
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()
        self.assertEqual(len(u1.get_prev_enrolled()), 0)
        self.assertEqual(len(u2.get_prev_enrolled()), 0)
        pe1 = Past_Enrollments(student_id=u1.id, course_id=c1.id, grade_earned='A', sa_before=True, term='2023A')
        pe2 = Past_Enrollments(student_id=u1.id, course_id=c2.id, grade_earned='B', sa_before=False, term='2023C')
        pe3 = Past_Enrollments(student_id=u2.id, course_id=c1.id, grade_earned='B', sa_before=True, term='2023C')
        db.session.add(pe1)
        db.session.add(pe2)
        db.session.add(pe3)
        db.session.commit()
        
        self.assertEqual(len(u1.get_prev_enrolled()), 2)
        self.assertEqual(u1.get_prev_enrolled()[1].course.num, 'CS2223')
        self.assertEqual(u1.get_prev_enrolled()[1].course.title, 'Algorithms')
        self.assertEqual(u1.get_prev_enrolled()[1].grade_earned, 'B')
        self.assertEqual(u1.get_prev_enrolled()[1].sa_before, False)
        self.assertEqual(u1.get_prev_enrolled()[1].term, '2023C')
        
        self.assertEqual(len(u2.get_prev_enrolled()), 1)
        self.assertEqual(u2.get_prev_enrolled()[0].course.num, 'CS3733')
        self.assertEqual(u2.get_prev_enrolled()[0].course.title, 'Soft Eng')
        self.assertEqual(u2.get_prev_enrolled()[0].grade_earned, 'B')
        self.assertEqual(u2.get_prev_enrolled()[0].sa_before, True)
        self.assertEqual(u2.get_prev_enrolled()[0].term, '2023C')

    def test_apply_1(self):
        u1 = Student(email='quan@wpi.edu',
                       first_name='Quan',
                       last_name='Dinh',
                       wpi_id='123456789',
                       phone='123456789',
                       user_type = 'Student',
                       major='CS',
                       gpa=4,
                       grad_date=datetime.now())
        db.session.add(u1)
        db.session.commit()
        i1 = Instructor(email='instr@wpi.edu',
                       first_name='Instructor',
                       last_name='One',
                       wpi_id='789561564',
                       phone='789456123',
                       user_type = 'Instructor')
        db.session.add(i1)
        db.session.commit()
        
        c1 = Course(num='CS3733', title="Soft Eng")
        c2 = Course(num='CS2223', title="Algorithms")
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()
        
        s1 = Section(instructor_id=i1.id, course_id=c1.id, section_num='01', term ='2024C')
        db.session.add(s1)
        db.session.commit()
        p1 = Position(section_id=s1.id, min_GPA=4, prev_sa_exp=False, max_SA=2)
        db.session.add(p1)
        db.session.commit()
        
        a1 = Application(student_id=u1.id, position_id=p1.id)
        db.session.add(a1)
        db.session.commit()
        
        self.assertEqual(len(i1.get_all_applications()), 1)
        self.assertEqual(i1.get_all_applications()[0].applicant.id, u1.id)
        self.assertEqual(i1.get_all_applications()[0].status, 'Pending')
        self.assertEqual(len(u1.get_all_applications()), 1)
        self.assertEqual(u1.get_all_applications()[0].applied_to.id, p1.id)
        self.assertEqual(u1.get_all_applications()[0].status, 'Pending')
        
    def test_apply_2(self):
        u1 = Student(email='quan@wpi.edu',
                       first_name='Quan',
                       last_name='Dinh',
                       wpi_id='123456789',
                       phone='123456789',
                       user_type = 'Student',
                       major='CS',
                       gpa=4,
                       grad_date=datetime.now())
        u2 = Student(email='christine@wpi.edu',
                       first_name='Christine',
                       last_name='Mae',
                       wpi_id='987654321',
                       phone='9876654321',
                       user_type = 'Student',
                       major='DS',
                       gpa=3.5,
                       grad_date=datetime.now())
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        i1 = Instructor(email='instr@wpi.edu',
                       first_name='Instructor',
                       last_name='One',
                       wpi_id='789561564',
                       phone='789456123',
                       user_type = 'Instructor')
        i2 = Instructor(email='instr2@wpi.edu',
                       first_name='Instructor',
                       last_name='Two',
                       wpi_id='789456123',
                       phone='789456165',
                       user_type = 'Instructor')
        db.session.add(i1)
        db.session.add(i2)
        db.session.commit()
        
        c1 = Course(num='CS3733', title="Soft Eng")
        c2 = Course(num='CS2223', title="Algorithms")
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()
        
        s1 = Section(instructor_id=i1.id, course_id=c1.id, section_num='01', term ='2024C')
        s2 = Section(instructor_id=i2.id, course_id=c2.id, section_num='02', term ='2024B')
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()
        p1 = Position(section_id=s1.id, min_GPA=4, prev_sa_exp=False, max_SA=2)
        p2 = Position(section_id=s2.id, min_GPA=3, prev_sa_exp=True, max_SA=3)
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()
        
        a1 = Application(student_id=u1.id, position_id=p1.id)
        a2 = Application(student_id=u1.id, position_id=p2.id)
        a3 = Application(student_id=u2.id, position_id=p1.id)
        db.session.add(a1)
        db.session.add(a2)
        db.session.add(a3)
        db.session.commit()
        
        self.assertEqual(len(i1.get_all_applications()), 2)
        self.assertEqual(i1.get_all_applications()[1].applicant.id, u2.id)
        self.assertEqual(i1.get_all_applications()[1].status, 'Pending')
        self.assertEqual(len(i2.get_all_applications()), 1)
        self.assertEqual(i2.get_all_applications()[0].applicant.id, u1.id)
        self.assertEqual(i2.get_all_applications()[0].status, 'Pending')
        
        self.assertEqual(len(u1.get_all_applications()), 2)
        self.assertEqual(u1.get_all_applications()[1].applied_to.id, p2.id)
        self.assertEqual(u1.get_all_applications()[1].status, 'Pending')
        self.assertEqual(len(u2.get_all_applications()), 1)
        self.assertEqual(u2.get_all_applications()[0].applied_to.id, p1.id)
        self.assertEqual(u2.get_all_applications()[0].status, 'Pending')

    def test_assign_1(self):
        u1 = Student(email='quan@wpi.edu',
                       first_name='Quan',
                       last_name='Dinh',
                       wpi_id='123456789',
                       phone='123456789',
                       user_type = 'Student',
                       major='CS',
                       gpa=4,
                       grad_date=datetime.now())
        db.session.add(u1)
        db.session.commit()
        i1 = Instructor(email='instr@wpi.edu',
                       first_name='Instructor',
                       last_name='One',
                       wpi_id='789561564',
                       phone='789456123',
                       user_type = 'Instructor')
        db.session.add(i1)
        db.session.commit()
        
        c1 = Course(num='CS3733', title="Soft Eng")
        c2 = Course(num='CS2223', title="Algorithms")
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()
        
        s1 = Section(instructor_id=i1.id, course_id=c1.id, section_num='01', term ='2024C')
        db.session.add(s1)
        db.session.commit()
        p1 = Position(section_id=s1.id, min_GPA=4, prev_sa_exp=False, max_SA=2)
        db.session.add(p1)
        db.session.commit()
        
        a1 = Application(student_id=u1.id, position_id=p1.id)
        db.session.add(a1)
        db.session.commit()
        
        status = i1.assign_sa(p1.id, u1.id)
        
        self.assertEqual(i1.get_all_applications()[0].status, 'Assigned')
        self.assertEqual(u1.get_all_applications()[0].status, 'Assigned')
        self.assertTrue(status)
        self.assertEqual(u1.get_sa_section().id, s1.id)
    
    def test_assign_2(self):
        u1 = Student(email='quan@wpi.edu',
                       first_name='Quan',
                       last_name='Dinh',
                       wpi_id='123456789',
                       phone='123456789',
                       user_type = 'Student',
                       major='CS',
                       gpa=4,
                       grad_date=datetime.now())
        u2 = Student(email='christine@wpi.edu',
                       first_name='Christine',
                       last_name='Mae',
                       wpi_id='987654321',
                       phone='9876654321',
                       user_type = 'Student',
                       major='DS',
                       gpa=3.5,
                       grad_date=datetime.now())
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        i1 = Instructor(email='instr@wpi.edu',
                       first_name='Instructor',
                       last_name='One',
                       wpi_id='789561564',
                       phone='789456123',
                       user_type = 'Instructor')
        i2 = Instructor(email='instr2@wpi.edu',
                       first_name='Instructor',
                       last_name='Two',
                       wpi_id='789456123',
                       phone='789456165',
                       user_type = 'Instructor')
        db.session.add(i1)
        db.session.add(i2)
        db.session.commit()
        
        c1 = Course(num='CS3733', title="Soft Eng")
        c2 = Course(num='CS2223', title="Algorithms")
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()
        
        s1 = Section(instructor_id=i1.id, course_id=c1.id, section_num='01', term ='2024C')
        s2 = Section(instructor_id=i2.id, course_id=c2.id, section_num='02', term ='2024B')
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()
        p1 = Position(section_id=s1.id, min_GPA=4, prev_sa_exp=False, max_SA=2)
        p2 = Position(section_id=s2.id, min_GPA=3, prev_sa_exp=True, max_SA=3)
        db.session.add(p1)
        db.session.add(p2)
        db.session.commit()
        
        a1 = Application(student_id=u1.id, position_id=p1.id)
        a2 = Application(student_id=u1.id, position_id=p2.id)
        a3 = Application(student_id=u2.id, position_id=p1.id)
        db.session.add(a1)
        db.session.add(a2)
        db.session.add(a3)
        db.session.commit()
        
        status1 = i1.assign_sa(p1.id, u1.id)
        status2 = i2.assign_sa(p2.id, u1.id)
        status3 = i1.assign_sa(p1.id, u2.id)
        
        self.assertEqual(i1.get_all_applications()[0].status, 'Assigned')
        self.assertEqual(u1.get_all_applications()[0].status, 'Assigned')
        self.assertEqual(u1.get_sa_section().id, s1.id)
        self.assertTrue(status1)
        # Check student already assigned, cannot be assigned to another position
        self.assertEqual(i2.get_all_applications()[0].status, 'Pending')
        self.assertEqual(u1.get_all_applications()[1].status, 'Pending')
        self.assertFalse(status2)
        # Check another student assigned to the same position
        self.assertEqual(i1.get_all_applications()[1].status, 'Assigned')
        self.assertEqual(u2.get_all_applications()[0].status, 'Assigned')
        self.assertEqual(u2.get_sa_section().id, s1.id)
        self.assertTrue(status3)
    
    def test_assign_3(self):
        u1 = Student(email='quan@wpi.edu',
                       first_name='Quan',
                       last_name='Dinh',
                       wpi_id='123456789',
                       phone='123456789',
                       user_type = 'Student',
                       major='CS',
                       gpa=4,
                       grad_date=datetime.now())
        u2 = Student(email='christine@wpi.edu',
                       first_name='Christine',
                       last_name='Mae',
                       wpi_id='987654321',
                       phone='9876654321',
                       user_type = 'Student',
                       major='DS',
                       gpa=3.5,
                       grad_date=datetime.now())
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        i1 = Instructor(email='instr@wpi.edu',
                       first_name='Instructor',
                       last_name='One',
                       wpi_id='789561564',
                       phone='789456123',
                       user_type = 'Instructor')
        db.session.add(i1)
        db.session.commit()
        
        c1 = Course(num='CS3733', title="Soft Eng")
        db.session.add(c1)
        db.session.commit()
        
        s1 = Section(instructor_id=i1.id, course_id=c1.id, section_num='01', term ='2024C')
        db.session.add(s1)
        db.session.commit()
        p1 = Position(section_id=s1.id, min_GPA=4, prev_sa_exp=False, max_SA=1)
        db.session.add(p1)
        db.session.commit()
        
        a1 = Application(student_id=u1.id, position_id=p1.id)
        a2 = Application(student_id=u2.id, position_id=p1.id)
        db.session.add(a1)
        db.session.add(a2)
        db.session.commit()
        
        status1 = i1.assign_sa(p1.id, u1.id)
        status2 = i1.assign_sa(p1.id, u2.id)
        
        self.assertEqual(i1.get_all_applications()[0].status, 'Assigned')
        self.assertEqual(u1.get_all_applications()[0].status, 'Assigned')
        self.assertTrue(status1)
        # Check the position is full so cannot assigned another student
        self.assertEqual(i1.get_all_applications()[1].status, 'Pending')
        self.assertEqual(u2.get_all_applications()[0].status, 'Pending')
        self.assertFalse(status2)
        self.assertEqual(p1.max_SA, p1.curr_SA)

    def test_withdraw_1(self):
        u1 = Student(email='quan@wpi.edu',
                       first_name='Quan',
                       last_name='Dinh',
                       wpi_id='123456789',
                       phone='123456789',
                       user_type = 'Student',
                       major='CS',
                       gpa=4,
                       grad_date=datetime.now())
        db.session.add(u1)
        db.session.commit()
        i1 = Instructor(email='instr@wpi.edu',
                       first_name='Instructor',
                       last_name='One',
                       wpi_id='789561564',
                       phone='789456123',
                       user_type = 'Instructor')
        db.session.add(i1)
        db.session.commit()
        
        c1 = Course(num='CS3733', title="Soft Eng")
        db.session.add(c1)
        db.session.commit()
        
        s1 = Section(instructor_id=i1.id, course_id=c1.id, section_num='01', term ='2024C')
        db.session.add(s1)
        db.session.commit()
        p1 = Position(section_id=s1.id, min_GPA=4, prev_sa_exp=False, max_SA=2)
        db.session.add(p1)
        db.session.commit()
        
        a1 = Application(student_id=u1.id, position_id=p1.id)
        db.session.add(a1)
        db.session.commit()
        
        self.assertEqual(len(i1.get_all_applications()), 1)
        self.assertEqual(len(u1.get_all_applications()), 1)

        u1.withdraw(p1.id)
        
        self.assertEqual(len(i1.get_all_applications()), 0)
        self.assertEqual(len(u1.get_all_applications()), 0)
        
    def test_withdraw_2(self):
        u1 = Student(email='quan@wpi.edu',
                       first_name='Quan',
                       last_name='Dinh',
                       wpi_id='123456789',
                       phone='123456789',
                       user_type = 'Student',
                       major='CS',
                       gpa=4,
                       grad_date=datetime.now())
        db.session.add(u1)
        db.session.commit()
        i1 = Instructor(email='instr@wpi.edu',
                       first_name='Instructor',
                       last_name='One',
                       wpi_id='789561564',
                       phone='789456123',
                       user_type = 'Instructor')
        db.session.add(i1)
        db.session.commit()
        
        c1 = Course(num='CS3733', title="Soft Eng")
        db.session.add(c1)
        db.session.commit()
        
        s1 = Section(instructor_id=i1.id, course_id=c1.id, section_num='01', term ='2024C')
        db.session.add(s1)
        db.session.commit()
        p1 = Position(section_id=s1.id, min_GPA=4, prev_sa_exp=False, max_SA=2)
        db.session.add(p1)
        db.session.commit()
        
        a1 = Application(student_id=u1.id, position_id=p1.id)
        db.session.add(a1)
        db.session.commit()
        
        i1.assign_sa(p1.id, u1.id)

        status = u1.withdraw(p1.id)
        
        # Check cannot withdraw if student is already assigned
        self.assertEqual(len(i1.get_all_applications()), 1)
        self.assertEqual(len(u1.get_all_applications()), 1)
        self.assertFalse(status)
        
        
    
if __name__ == '__main__':
    unittest.main(verbosity=1)