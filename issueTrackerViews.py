from flask import render_template, Blueprint, redirect, request, session
# from flask_session import Session
# from tempfile import mkdtemp
import sqlite3
from helpers import apology, login_required



#issueTrack = Blueprint('issueTrack', __name__, url_prefix='/issue', template_folder='templates', static_folder='static')
# This one will work for local testing
issueTrack = Blueprint('issueTrack', __name__, url_prefix='/', template_folder='templates', static_folder='static')

# This function helps convert list of tuple output of sql query into list of dictionaries output
# Taken from https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Connect to database todo don't know if checksamethread=false is bad practice
connection = sqlite3.connect("./static/IssueTracker.db", check_same_thread=False)
connection.row_factory = dict_factory
db = connection.cursor()
# do queries like this:
var = db.execute("SELECT * FROM Access")
var = var.fetchall()
print(var)

@issueTrack.route('/', methods=['GET', 'POST'])
def index():
    # Forget user_id
    session.clear()
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
        # Check database for username
        rows = db.execute("SELECT * FROM Users WHERE Username = ?", (request.form.get("username"),))
        rows = rows.fetchall()
        print(rows)
        if len(rows) !=1 or not rows[0]["Password"] == request.form.get("password"):
            return apology("Invalid Username and/or Password")
        # Remember which user has logged in
        session["user_id"] = rows[0]["Username"]

        # Redirect user to home page
        # todo we don't have this yet
        # return redirect("/homepage")
        return render_template("login.html")
    else:
        return render_template("login.html")

@issueTrack.route('/register')
def register():
    return render_template("register.html")