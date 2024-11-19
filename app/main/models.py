from datetime import datetime, timezone
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

courseSA = db.Table(
    'courseSA',
    db.metadata,
    sqla.Column('course_id', sqla.Integer, sqla.ForeignKey('course.id'), primary_key=True),
    sqla.Column('sa_id', sqla.Integer, sqla.ForeignKey('student.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    username: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64), unique=True)
    email: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120), unique=True)
    wpi_id: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(9), unique=True)
    phone: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(20))
    password_hash: sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(256))
    user_type : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'User',
        'polymorphic_on':user_type
    }
    
    def __repr__(self):
        return '<Id {} : {} >'.format(self.id,self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class Instructor(User):
    __tablename__='instructor'
    id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id), primary_key=True)
    
    sections : sqlo.WriteOnlyMapped['Section'] = sqlo.relationship(back_populates= 'instructor')
    
    positions: sqlo.WriteOnlyMapped['Position'] = sqlo.relationship(back_populates="instructor")

    
    __mapper_args__ = {
        'polymorphic_identity': 'Instructor'
    }
    
    def get_sections(self):
        return db.session.scalars(self.sections.select()).all()
    
    
class Student(User):
    __tablename__='student'
    id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id), primary_key=True)
    major: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64))
    gpa: sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float)
    grad_date: sqlo.Mapped[datetime] = sqlo.mapped_column(sqla.DateTime)
    
    # Relationships
    served_courses: sqlo.WriteOnlyMapped['Course'] = sqlo.relationship(
        secondary=courseSA,
        primaryjoin=(courseSA.c.course_id == id),
        back_populates='served_sas'
    )
    course_applied: sqlo.WriteOnlyMapped['Application'] = sqlo.relationship(back_populates='applicant')
    
    __mapper_args__ = {
        'polymorphic_identity': 'Student'
    }
    
    def get_major(self):
        return self.major

    def get_gpa(self):
        return self.gpa
    
    def get_grad_date(self):
        return self. grad_date
    
    
class Course(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    num: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(10), unique=True)
    title: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(100), unique=True)
    
    # Relationships
    served_sas: sqlo.WriteOnlyMapped['Student'] = sqlo.relationship(
        secondary=courseSA,
        primaryjoin=(courseSA.c.sa_id == id),
        back_populates='served_courses'
    )
    
    def get_num(self):
        return self.num
    
    def get_gpa(self):
        return self.title
    
    has_sections : sqlo.Mapped['Section'] = sqlo.relationship(back_populates= 'in_course')
    
class Section(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    instructor_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Instructor.id), index=True)
    course_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Course.id), index=True)
    section_num: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5))
    term: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5))
    
    max_SA: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, default=0)
    curr_SA: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, default=0)
    min_GPA: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, default=0)
    min_grade: sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(5))
    
    instructor : sqlo.Mapped[Instructor] = sqlo.relationship(back_populates= 'sections')
    in_course: sqlo.Mapped[Course] = sqlo.relationship(back_populates= 'has_sections')
    section_application: sqlo.WriteOnlyMapped['Application'] = sqlo.relationship(back_populates='applied_section')
    positions: sqlo.WriteOnlyMapped['Position'] = sqlo.relationship(back_populates="in_section")


    __table_args__ = (
        sqla.UniqueConstraint('course_id', 'section_num', 'term', name='uix_course_section_term'),
    )
    
class Application(db.Model):
    student_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Student.id), primary_key=True)
    section_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Section.id), primary_key=True)
    term: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5))
    grade: sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(5))
    status: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(20))
    
    applicant: sqlo.Mapped[Student] = sqlo.relationship(back_populates='course_applied')
    applied_section: sqlo.Mapped[Section] = sqlo.relationship(back_populates='section_application')
    
    def __repr__(self):
        return f"<Application(student_id={self.student_id}, section_id={self.section_id}, term={self.term}, status={self.status})>"
    
class Position(db.Model):
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    instructor_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Instructor.id))
    course_section_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Section.id))
    min_GPA: sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float)
    min_grade: sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float)
    term: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5))
    SA_num: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer)
    
    instructor: sqlo.Mapped[Instructor] = sqlo.relationship(back_populates="positions")
    in_section: sqlo.Mapped[Section] = sqlo.relationship(back_populates="positions")
    
    def __repr__(self):
        return f"<Position(section_id={self.section_id}, sa_id={self.sa_id}, term={self.term}, year={self.year})>"
