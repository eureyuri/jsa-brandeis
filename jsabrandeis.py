from flask import Flask, render_template, request, flash, redirect, url_for
from sendGrid import send
from flask_login import LoginManager, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


# TODO: Check on heroku if this works
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')
app.secret_key = os.environ.get('FLASK_KEY')

db = SQLAlchemy(app)

import model

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'


@app.errorhandler(404)
def page_not_found(e):
    # TODO
    print(e)
    return "404"


@app.route('/', methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def contact():
    subject = "JSA - Contact"
    message = "Name: " + str(request.form["name"]) + "\nEmail: " + str(request.form["email"]) \
                   + "\nComment: " + (request.form["comment"])
    send(subject, message)

    return render_template("index.html")


@app.route('/news', methods=["GET"])
def news():
    return render_template("news.html")


@app.route('/pastEvents', methods=["GET"])
def pastEvents():
    return render_template("past_events.html")


@app.route('/involve', methods=["GET"])
def involve():
    return render_template("involve.html")


@app.route('/involve', methods=['POST'])
def volunteer():
    subject = "JSA - Volunteer"
    message = "Name: " + str(request.form["name"]) + "\nEmail: " + str(request.form["email"]) \
              + "\nComment: " + (request.form["comment"])
    send(subject, message)

    return render_template("involve.html")


@app.route('/outsideBrandeis', methods=["GET"])
def outside_brandeis():
    return render_template("outsidebrandeis.html")


@app.route('/login', methods=["GET"])
def login():
    return render_template("login.html")


@app.route('/login', methods=['POST'])
def logged_in():
    email = str(request.form['email'])
    password = str(request.form['password'])
    user_match_db = model.User.query.filter_by(email=email).first()

    if user_match_db is not None and user_match_db.is_correct_password(password):
        user_match_db.authenticated = True
        # db.session.add(user_match_db)
        # db.session.commit()
        # login_user(user_match_db)
        # flash('Thanks for logging in, {}'.format(user_match_db.email))
        return redirect(url_for('admin'))
    else:
        flash('ERROR! Incorrect login credentials!')
        return render_template("login.html")


@app.route('/admin', methods=['GET'])
# @login_required
def admin():
    return render_template("admin.html")


@login_manager.user_loader
def load_user(user_id):
    """
    Given *user_id*, return the associated User object.
    :param unicode user_id: user_id (email) user to retrieve
    """
    return model.User.query.filter(model.User.id == int(user_id)).first()


if __name__ == '__main__':
    app.run()