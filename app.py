import os

from io import StringIO
import csv
from flask import make_response
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///tasks.db")

@app.route("/closed_task")
@login_required
def closed_task():
    """Show history of transactions"""
    tasks = db.execute("SELECT id, time, team, room_number, room_location, detail, status FROM tasks WHERE status = 'closed'")
    return render_template("closed_task.html", tasks=tasks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        #Get variables from the forms
        name = request.form.get("username")

        usercheck = db.execute("SELECT * FROM users WHERE username = ?", name)

        password = request.form.get("password")

        team = request.form.get("team")

        passwordcheck = request.form.get("confirmation")
        #Check if username is taken
        if len(usercheck) != 0:
            return apology("Username already in use", 400)
        #Check if user gave an username and a password
        if not request.form.get("username") or not request.form.get("password") or not request.form.get("team"):
            return apology("Provide an username, password and team", 400)
        #Check if password fields match
        if (password != passwordcheck):
            return apology("Please make sure password fields match", 400)

        else:
            #hash the password
            hashed = generate_password_hash(password)
            #Write data into D
            db.execute("INSERT INTO users (username, hash, team) VALUES (?, ?, ?)", name, hashed, team)

            return redirect("/login")

    return render_template("register.html")

@app.route("/new_task", methods=["GET", "POST"])
@login_required
def new_task():
    
    if request.method == "POST":
        user_id = session["user_id"]
        team = request.form.get("team")
        room_number = request.form.get("room_number")
        room_location = request.form.get("room_location")
        detail = request.form.get("detail")
        status = "open"

        if team is None or room_number is None or room_location is None or detail is None:
            return apology("Please provide information in all fields")
        
        else:
            db.execute("INSERT INTO tasks(user_id, team, room_number, room_location, detail, status) VALUES (?,?,?,?,?,?)", user_id, team, room_number, room_location, detail, status)
            return redirect("/")

    return render_template("new_task.html")    

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        task_id = request.form.get("value")
        db.execute("UPDATE tasks SET status = 'closed' WHERE id = ?", task_id)

    tasks = db.execute("SELECT id, time, team, room_number, room_location, detail, status FROM tasks WHERE status = ? ORDER BY time ASC", "open")
    return render_template("index.html", tasks=tasks)

@app.route("/report", methods=["GET", "POST"])
@login_required
def report():
    if request.method == "POST":
        date_from = request.form.get("date_from")
        date_to = request.form.get("date_to") + '23:59:59'
        team = request.form.get("team")

        if not request.form.get("team"):
            team = "team"

        if not request.form.get("date_from") or not request.form.get("date_to") or (date_from > date_to):
            return apology("please provide a valid time period")

        else:
            reports = db.execute("SELECT * FROM tasks WHERE team = ? AND time BETWEEN ? AND ?", team, date_from, date_to)
            return render_template("reported.html", reports=reports)


    else:
        return render_template("reports.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
