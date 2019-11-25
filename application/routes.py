from flask import current_app as app
from flask import render_template, flash, redirect
from application.forms import LoginForm

from .mentor_view import MentorApi
app.register_blueprint(MentorApi, url_prefix='/mentor')

# from .admin_view import AdminApi
# app.register_blueprint(AdminApi, url_prefix='/admin')




@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John Doe'},
            'body': 'Welcome to your Mentor Portal!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)