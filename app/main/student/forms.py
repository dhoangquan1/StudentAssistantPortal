from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField, FloatField
from wtforms.validators import  ValidationError, DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

from app import db
import sqlalchemy as sqla
from app.main.models import Application, Position


class ApplicationForm(FlaskForm):
    grade = SelectField('Grade Earned', choices = [('A', 'A'), ('B', 'B'), ('C', 'C') ])
    year_took_course = StringField('Year course was taken', validators=[DataRequired()])
    term_took_course = SelectField('Term course was taken', choices = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),  ('E', 'E')])
    year_to_apply = StringField('Applying year', validators=[DataRequired()])
    term_to_apply = SelectField('Applying term', choices = [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),  ('E', 'E')])
    # term_to = QuerySelectMultipleField(
    #     'Select available term',
    #     query_factory = lambda : db.session.scalars(sqla.select)
    #     )
    submit = SubmitField('Create')