from flask import Flask, render_template, request, flash
from sendGrid import send
from flask_login import LoginManager, login_user
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')

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


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        print("HELLO")
        email = str(request.form['email'])
        password = str(request.form['password'])
        print(email)
        print(password)
        return render_template("involve.html")


@app.route('/login', methods=['POST'])
def logged_in():
    print("HERE")
    email = str(request.form['email'])
    password = str(request.form['pwd'])
    # user1 = user.User.query.filter_by(email=email).first()
    print(email)
    print(password)
    return render_template("involve.html")

    # if user1 is not None and user1.is_correct_password(password):
    #     print("HERE1")
    #     user1.authenticated = True
    #     db.session.add(user)
    #     db.session.commit()
    #     login_user(user1)
    #     flash('Thanks for logging in, {}'.format(user1.email))
    #     return render_template("involve.html")
    # else:
    #     print("HERE2")
    #     flash('ERROR! Incorrect login credentials.', 'error')
    #     return render_template("index.html")


@login_manager.user_loader
def load_user(user_id):
    """
    Given *user_id*, return the associated User object.
    :param unicode user_id: user_id (email) user to retrieve
    """
    return model.User.query.filter(model.User.id == int(user_id)).first()


if __name__ == '__main__':
    app.run()