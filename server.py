"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/register', methods=["GET"])
def register_form():
    """Show the register form"""

    return render_template("register_form.html")

@app.route('/register', methods=["POST"])
def register_process():

    #Get the info
    #Create a user in the DB, store it
    email = request.form.get("email")
    password = request.form.get("password")

    #queryDB for email
    #if email in DB and PW matches, return redirect login
    #else - create account, add to DB

    match = User.query.filter_by(email=email).first()

    if match == None:
        user = User(email=email,
                    password=password)
        db.session.add(user)
        db.session.commit()
        return redirect("/")
    elif match.email == email:
        if match.password == password:
            return redirect("/login")
        else:
            flash("That password is incorrect")
            return redirect("/register")


        
    







if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
