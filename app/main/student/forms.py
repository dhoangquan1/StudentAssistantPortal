from datetime import datetime, timezone

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

    def validate_year_took_course(self, year_took_course):
        if not (year_took_course.data.isnumeric()):
            raise ValidationError('Year input is not valid')
        year = datetime.now(timezone.utc).year
        if int(year_took_course.data) > year or int(year_took_course.data) < 1865:
            raise ValidationError('This year is not valid')
    
class SortForm(FlaskForm):
    choice = SelectField('Sort by',
                        choices=[
                            ('min_GPA', 'Minimum GPA (ascending)'),
                            ('min_grade', 'Minimum Grade (ascending)')
                        ])
    prev_exp = BooleanField('Requires previous Student Assistant experience')
    submit = SubmitField('Refresh')