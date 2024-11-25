from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, BooleanField, FloatField
from wtforms.validators import  ValidationError, DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectMultipleField, QuerySelectField
from wtforms.widgets import ListWidget, CheckboxInput

from app import db
import sqlalchemy as sqla
from app.main.models import Application, Position


class ApplicationForm(FlaskForm):
    grade = SelectField('Grade Earned', choices = [
        'A', 'B', 'C' 
    ])
    year_took_course = StringField('Year course was taken', validators=[DataRequired()])
    term_took_course = SelectField('Term course was taken', choices = ['A', 'B', 'C', 'D', 'E'])
    year_to_apply = StringField('Applying year', validators=[DataRequired()])
    term_to_apply = QuerySelectField(
        'Select available term',
        query_factory = None,
        get_label=None
        )
    submit = SubmitField('Apply')
    
    def __init__(self, position_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically update the query factory based on the position_id
        self.term_to_apply.query_factory = lambda: db.session.scalars(
            sqla.select(Position).where(Position.id == position_id)
        )
        self.term_to_apply.get_label = lambda position : position.get_section_term()