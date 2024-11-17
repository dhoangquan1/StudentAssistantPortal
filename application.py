from config import Config

from app import create_app, db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

from app.main.models import Course

app = create_app(Config)

@app.shell_context_processor
def make_shell_context():
    return {'sqla': sqla, 'sqlo': sqlo, 'db': db, 'Course' : Course}

@app.before_request
def initDB(*args, **kwargs):
    if app._got_first_request:
        db.create_all()
        query = sqla.select(Course)
        if db.session.scalars(query).first() is None:
            courses = [{'num':'CS1101','title':'Introduction To Program Design'},
            {'num':'CS2022','title':'Discrete Mathematics'},
            {'num':'CS2223','title':'Algorithms'},
            {'num':'CS3013','title':'Operating Systems'}, 
            {'num':'CS3431','title': 'Database Systems I'}]
            for c in courses:
                db.session.add(Course(num = c['num'], title = c['title']))
            db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)