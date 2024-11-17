from flask import Blueprint

student_blueprint = Blueprint('student', __name__)

from app.main.student import routes