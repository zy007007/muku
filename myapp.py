import models
from flask import Flask
from views import login, student, main, homework, test, spoc, course
from config.ext import db, bootstrap, user_login_manager, mongo
from flask_script import Shell, Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbuser:Changeme_123@postgres/muke'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'xxx'

app.config['MONGODB_DB'] = 'muke'
app.config['MONGODB_HOST'] = 'mongo'
app.config['MONGODB_PORT'] = 27017

db.init_app(app)
bootstrap.init_app(app)
user_login_manager.init_app(app)
mongo.init_app(app)

app.register_blueprint(login.bp)
app.register_blueprint(main.bp)
app.register_blueprint(student.bp)
app.register_blueprint(homework.bp)
app.register_blueprint(test.bp)
app.register_blueprint(spoc.bp)
app.register_blueprint(course.bp)

manager = Manager(app)


def make_shell_context():
    return dict(app=app, db=db, models=models)

migrate = Migrate(app, db)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()



