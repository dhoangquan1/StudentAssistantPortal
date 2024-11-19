from flask_login import current_user
from flask_wtf import FlaskForm
import sqlalchemy as sqla
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired,NumberRange,Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.widgets import ListWidget,CheckboxInput

from app import db
from app.main.models import Section,Course
class PositionForm(FlaskForm):
    section = QuerySelectField('Course Section', 
                         query_factory=lambda: db.session.scalars(sqla.select(Section).join(Section.in_course).order_by(Course.title)),
                         get_label=lambda section: section.in_course.title,
                         allow_blank=False
                         )
    SAnum = IntegerField('Amount of SA:',validators=[DataRequired(), NumberRange(min=1, max=9999)])
    minGPA = FloatField('Minimum GPA:',validators=[DataRequired(), NumberRange(min=0, max=4)])  
    min_grade = FloatField('Minimum grade for the course:',validators=[DataRequired(), NumberRange(min=0, max=4)])
    term = StringField('Term:', validators=[DataRequired()])
    submit = SubmitField('Create Positions')
                         

