from config import Config

from app import create_app, db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

from app.main.models import Course, Student, Past_Enrollments

from werkzeug.middleware.proxy_fix import ProxyFix
import identity.web

app = create_app(Config)

app.jinja_env.globals.update(Auth=identity.web.Auth)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.shell_context_processor
def make_shell_context():
    return {'sqla': sqla, 'sqlo': sqlo, 'db': db, 'Course' : Course, 'Student' : Student, 'Past_Enrollments' : Past_Enrollments}

@app.before_request
def initDB(*args, **kwargs):
    if app._got_first_request:
        db.create_all()
        query = sqla.select(Course)
        if db.session.scalars(query).first() is None:
            courses = [
                {'num':'CS1101','title':'Introduction To Program Design'},
                {'num':'CS2022','title':'Discrete Mathematics'},
                {'num':'CS2102','title':'Object-Oriented Design Concepts'},
                {'num':'CS2223','title':'Algorithms'},
                {'num':'CS2303','title':'Systems Programming Concepts'},
                {'num':'CS3013','title':'Operating Systems'}, 
                {'num':'CS3043','title':'Social Implications of Information Processing'},
                {'num':'CS3133','title':'Foundations Of Computer Science'},
                {'num':'CS3431','title':'Database Systems I'},
                {'num':'CS3733','title':'Software Engineering'},
            ]
            for c in courses:
                db.session.add(Course(num = c['num'], title = c['title']))
            db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)