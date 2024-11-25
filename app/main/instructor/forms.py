from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, IntegerField, FloatField, BooleanField, SelectField
from wtforms.validators import  ValidationError, DataRequired,NumberRange,Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.widgets import ListWidget, CheckboxInput

from app import db
import sqlalchemy as sqla
from app.main.models import Course, Section


class SectionForm(FlaskForm):
    course = QuerySelectField('Course',
                             query_factory = lambda : db.session.scalars(sqla.select(Course)),
                             get_label = lambda course : f"{course.num} - {course.title}",
                             allow_blank = False)
    section_num = StringField('Section Number', validators=[DataRequired()])
    term = StringField('Term', validators=[DataRequired()])
    submit = SubmitField('Create')
    
    def validate(self, extra_validators=None):
        if not super().validate():
            return False
        
        query = sqla.select(Section).where(
            Section.course_id == self.course.data.id,
            Section.section_num == self.section_num.data,
            Section.term == self.term.data,)
        section = db.session.scalars(query).first()
        
        if section is not None:
            self.course.errors.append('The section already exists, please choose a different course, section number, or term.')
            return False
        
        return True
    
class PositionForm(FlaskForm):
    section = QuerySelectField('Course Section', 
                         query_factory=lambda: db.session.scalars(current_user.sections.select()),
                         get_label=lambda section:  f"{section.in_course.num}-{section.section_num}: {section.in_course.title}",
                         allow_blank=False
                         )
    SAnum = IntegerField('Amount of Student Assistants:',validators=[DataRequired(), NumberRange(min=1, max=9999)])
    minGPA = FloatField('Minimum GPA',validators=[DataRequired(), NumberRange(min=0, max=4)])  
    min_grade = SelectField('Minimum grade for the course',choices = [(3, 'A'), (2, 'B'), (1,'C')], default=1)
    prev_sa_exp = BooleanField('Require previous SA experiences?')
    submit = SubmitField('Create Positions')