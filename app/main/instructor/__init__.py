from flask import Blueprint

instructor_blueprint = Blueprint('instructor', __name__)

from app.main.instructor import routes