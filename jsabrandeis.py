from flask import Flask, render_template, request, flash, redirect, url_for, session, g
from sendGrid import send
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from app_settings import app, db

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


import model

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


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
        # login_user(user_match_db)
        session['username'] = email
        # TODO: Implement remember button?
        # login_user(user_match_db, remember=True)
        return redirect(url_for('admin'))
    else:
        flash('ERROR! Incorrect login credentials!')
        return render_template("login.html")


@app.route("/logout", methods=["GET"])
# @login_required
def logout():
    if g.user:
        user = current_user
        user.authenticated = False
        # logout_user()
        session.pop('username', None)
        return redirect(url_for('index'))
    return redirect(url_for('login'))


@app.route('/admin', methods=['GET'])
# @login_required
def admin():
    if g.user:
        return render_template("admin.html")
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    return model.User.query.filter(model.User.email == user_id).first()


@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user = session['username']


@app.route('/add', methods=['GET'])
def add_display_user():
    if g.user:
        users = db.session.query(model.User.email).all()
        users = [user[0] for user in users]
        admin = False
        if g.user == 'admin@jsa':
            admin = True
        return render_template("add_user.html", users=users, admin=admin)
    return redirect(url_for('login'))


@app.route('/add', methods=['POST'])
def add_user():
    if g.user:
        email = str(request.form['email'])
        password = str(request.form['password'])
        new_user = model.User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('add_display_user'))
    return redirect(url_for('login'))


@app.route('/delete', methods=['POST'])
def delete_user():
    if g.user:
        if g.user == 'admin@jsa':
            email = str(request.form['email'])
            deleting_user = model.User.query.filter_by(email=email).first()
            if deleting_user:
                db.session.delete(deleting_user)
                db.session.commit()
        return redirect(url_for('add_display_user'))
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
