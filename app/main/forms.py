from flask_login import current_user
from flask_wtf import FlaskForm
import sqlalchemy as sqla
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired,NumberRange,Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.widgets import ListWidget,CheckboxInput

from app import db
from app.main.models import Section,Course,Position


