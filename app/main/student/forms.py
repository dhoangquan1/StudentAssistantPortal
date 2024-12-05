from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField, FloatField
from wtforms.validators import  ValidationError, DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from wtforms.widgets import ListWidget, CheckboxInput

from app import db
import sqlalchemy as sqla
from app.main.models import Application, Position


class ApplicationForm(FlaskForm):
    grade = SelectField('Grade Earned:', choices = [('A', 'A'), ('B', 'B'), ('C', 'C') ])
    year_took_course = StringField('Year course was taken', validators=[DataRequired()])
    term_took_course = SelectField('Term course was taken', choices = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),  ('E', 'E')])
    submit = SubmitField('Apply')
    
class SortForm(FlaskForm):
    choice = SelectField('Sort by',
                        choices=[
                            ('min_GPA', 'Minimum GPA (ascending)'),
                            ('min_grade', 'Minimum Grade (ascending)')
                        ])
    prev_exp = BooleanField('Requires previous Student Assistant experience')
    submit = SubmitField('Refresh')