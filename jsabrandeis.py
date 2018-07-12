from flask import Flask, render_template, request
from sendGrid import send


app = Flask(__name__)


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


if __name__ == '__main__':
    app.run()