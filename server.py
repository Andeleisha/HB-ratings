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

@app.route('/login', methods=["GET"])
def login_form():
    """Serves login form"""

    return render_template("login_form.html")

@app.route('/login', methods=["POST"])
def login():
    """Logs a user in if they provide the correct email and password"""

    #Check if email is in DB
    #   If it is, check if the password is correct
    #       If it is, log the user in
            # add the user ID to the flask SESSION
            # redirect to homepage, flash logged in
        #If PW not correct, flash message
    #If email not in DB, redirect to register

    #Add a login/logout button to base template 
    #Change text depending on if userID is in session
    #Links to login/logout page
    #Flashes logged in/logged out?

    email = request.form.get("email")
    password = request.form.get("password")

    match = User.query.filter_by(email=email).first()

    if match == None:
        flash("That user does not exist. Please create a new account.")
        return redirect("/register")
    elif match.email == email:
        if match.password == password:
            session["user"] = match.user_id
            print("The user's ID in the session is: {}".format(session["user"]))
            flash("You are now logged in.")
            return redirect("/user-detail/" + str(match.user_id))
        else:
            flash("That password is incorrect.")
            return redirect("/login")

@app.route('/logout', methods=["POST"])
def logout():
    """Logs a user out"""

    #Check if the user is in the session87
    #If yes, remove from session, redirect to home, flash message
    #If no, redirect to login page?
    if "user" in session:
        del session["user"]
        flash("You are logged out.")
        return redirect('/')
    else:
        flash("You are not logged in.")
        return redirect('/login')

@app.route("/user-detail/<user_id>")
def user_details(user_id):
    """Shows user info"""

    # user_id = request.args.get("user_id")

    user = User.query.filter_by(user_id=user_id).first()

    return render_template("user_details.html", user=user)

@app.route("/movies")
def movie_list():
    """Shows list of movies"""

    movies = Movie.query.all()

    return render_template("movie_list.html", movies=movies)


@app.route("/movie-detail/<movie_id>")
def movie_detail(movie_id):
    """Show details about a movie"""

    movie = Movie.query.filter_by(movie_id=movie_id).first()

    return render_template("movie_details.html", movie=movie)

@app.route("/rate-movie", methods=["POST"])
def rate_movie():
    """Handle the user rating """

    rating = request.form.get("rating")
    movie_id = request.form.get("movie_id")

    rating = int(rating)

    if "user" in session:
        user_id = session["user"]
        user = User.query.filter_by(user_id=user_id).first()
        newRating = Rating(movie_id=movie_id,
                        user_id=user_id,
                        score=rating)
        if Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first() == None:
            db.session.add(newRating)
            db.session.commit()
            return redirect("/")
        else:
            oldRating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()
            oldRating.score = rating
            db.session.commit()
            return redirect("/")
    else:
        flash("You must be logged in to rate a movie.")
        return redirect("/login")




        
    







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
