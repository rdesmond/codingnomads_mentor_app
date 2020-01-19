from application import create_app, db
from application.models import User, Student, Mentor
from flask.cli import FlaskGroup

app = create_app()

cli = FlaskGroup(create_app=create_app)

@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command('seed_db')
def seed_db():
    db.session.add(User(username='jonny', email='jonny@test.com'))
    db.session.add(User(username='kristen', email='kristen@test.com', is_student=True))
    db.session.commit()

if __name__ == "__main__":
    cli()