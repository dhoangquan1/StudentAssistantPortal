from datetime import datetime, timezone
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class User(UserMixin, db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    username: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64), unique=True)
    email: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120), unique=True)
    password_hash: sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(256))
    user_type : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'User',
        'polymorphic_on':user_type
    }
    
    def __repr__(self):
        return '<Id {} : {} >'.format(self.id,self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class Instructor(User):
    __tablename__='instructor'
    id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'Instructor'
    }
    
class Student(User):
    __tablename__='student'
    id: sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(User.id), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'Student'
    }