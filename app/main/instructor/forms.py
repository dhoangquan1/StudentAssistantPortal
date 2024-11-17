from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField
from wtforms.validators import  ValidationError, DataRequired, Length
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
            self.course.errors.append('The section is already exists, please choose a different course, section number, or term.')
            return False
        
        return True
    