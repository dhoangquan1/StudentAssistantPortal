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


class User(UserMixin, db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    email: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120), unique=True)
    first_name: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64))
    last_name: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64))
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
    
    def get_first_name(self):
        return self.first_name
    
    def get_last_name(self):
        return self.last_name
    

class Instructor(User):
    __tablename__='instructor'
    id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id), primary_key=True)
    
    sections : sqlo.WriteOnlyMapped['Section'] = sqlo.relationship(back_populates= 'instructor')
    
    __mapper_args__ = {
        'polymorphic_identity': 'Instructor'
    }
    
    def get_sections(self):
        return db.session.scalars(self.sections.select()).all()
    
    def get_positions(self):
        query  = sqla.select(Position).join(Section).where(self.id == Section.instructor_id)
        return db.session.scalars(query).all()
    
    def get_all_applications(self):
        query = (sqla.select(Application)
                 .join(Position).where(Position.id == Application.position_id)
                 .join(Section).where(Section.id == Position.section_id)
                 .where(Section.instructor_id == self.id))
        return db.session.scalars(query).all()
    
    def get_applications_by_position(self, position_id):
        query = (sqla.select(Application)
                 .join(Position).where(Position.id == position_id)
                 .join(Section).where(Section.id == Position.section_id)
                 .where(Section.instructor_id == self.id))
        return db.session.scalars(query).all()

    
class Student(User):
    __tablename__='student'
    id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id), primary_key=True)
    major: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64))
    gpa: sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float)
    grad_date: sqlo.Mapped[datetime] = sqlo.mapped_column(sqla.DateTime)
    
    # Relationships
    prev_enrolled: sqlo.WriteOnlyMapped['Past_Enrollments'] = sqlo.relationship(back_populates='student')
    pos_applied: sqlo.WriteOnlyMapped['Application'] = sqlo.relationship(back_populates='applicant')
    
    __mapper_args__ = {
        'polymorphic_identity': 'Student'
    }
    
    def __repr__(self):
        return '<Id {} : {} >'.format(self.id,super().username)
    
    def get_major(self):
        return self.major

    def get_gpa(self):
        return self.gpa
    
    def get_grad_date(self):
        return self.grad_date
    
    
    def get_prev_enrolled(self):
        return db.session.scalars(self.prev_enrolled.select()).all()
    
    
class Course(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    num: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(10), unique=True)
    title: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(100), unique=True)
    
    # Relationships
    has_sections : sqlo.Mapped['Section'] = sqlo.relationship(back_populates= 'in_course')
    prev_sa: sqlo.WriteOnlyMapped['Past_Enrollments'] = sqlo.relationship(back_populates='course')


class Past_Enrollments(db.Model):
    student_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Student.id), primary_key=True)
    course_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Course.id), primary_key=True)
    grade_earned: sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(5))
    sa_before: sqlo.Mapped[bool] = sqlo.mapped_column(sqla.Boolean, default=False)
    
    def __repr__(self):
        return '<Student {} took {} with grade {}, and had SA exp = {}>'.format(self.student_id,self.course_id,self.grade_earned, self.sa_before)
    
    # Relationships
    student: sqlo.Mapped[Student] = sqlo.relationship(back_populates='prev_enrolled')
    course: sqlo.Mapped[Course] = sqlo.relationship(back_populates='prev_sa')
    
class Section(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    instructor_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Instructor.id), index=True)
    course_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Course.id), index=True)
    section_num: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5))
    term: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(5))
    
    instructor : sqlo.Mapped[Instructor] = sqlo.relationship(back_populates= 'sections')
    in_course: sqlo.Mapped[Course] = sqlo.relationship(back_populates= 'has_sections')
    positions: sqlo.WriteOnlyMapped['Position'] = sqlo.relationship(back_populates="in_section")


    __table_args__ = (
        sqla.UniqueConstraint('course_id', 'section_num', 'term', name='uix_course_section_term'),
    )
    
class Position(db.Model):
    id: sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    section_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Section.id))
    
    min_GPA: sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float)
    min_grade: sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(5))
    prev_sa_exp: sqlo.Mapped[bool] = sqlo.mapped_column(sqla.Boolean)
    
    max_SA: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, default=0)
    curr_SA: sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, default=0)

    in_section: sqlo.Mapped[Section] = sqlo.relationship(back_populates="positions")
    applications: sqlo.WriteOnlyMapped['Application'] = sqlo.relationship(back_populates="applied_to")

    
    def __repr__(self):
        return f"<Position(section_id={self.section_id})>"

    def get_instructor_firstname(self):
        return self.in_section.instructor.first_name
    
    def get_instructor_lastname(self):
        return self.in_section.instructor.last_name
    
    def get_instructor_wpi_id(self):
        return self.in_section.instructor.wpi_id
    
    def get_instructor_email(self):
        return self.in_section.instructor.email
    
    def get_instructor_phone(self):
        return self.in_section.instructor.phone
    
    def check_apply_status(self, student_id):
        student = db.session.scalars(self.applications.select().where(Application.student_id == student_id)).first()
        return student is not None
    

class Application(db.Model):
    student_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Student.id), primary_key=True)
    position_id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Position.id), primary_key=True)
    status: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(20), default="Pending")
    
    applicant: sqlo.Mapped[Student] = sqlo.relationship(back_populates='pos_applied')
    applied_to: sqlo.Mapped[Position] = sqlo.relationship(back_populates='applications')
    
    def __repr__(self):
        return f"<Application(student_id={self.student_id}, section_id={self.position_id}, status={self.status})>"
    
    