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

        # Check if Demo account
        if request.form.get("admin"):
            session["user_id"] = "testadmin"
            return render_template('dashboard.html')
        elif request.form.get("user"):
            session["user_id"] = "testuser"
            return render_template('dashboard.html')
        # todo add the other two when they might matter

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
        # Check database for username
        rows = db.execute("SELECT * FROM Users WHERE Username = ?", (request.form.get("username"),))
        rows = rows.fetchall()
        # print(rows)
        if len(rows) !=1 or not rows[0]["Password"] == request.form.get("password"):
            return apology("Invalid Username and/or Password")
        # Remember which user has logged in
        session["user_id"] = rows[0]["Username"]

        # Redirect user to home page
        return redirect("/dashboard")
    else:
        return render_template("login.html")

# I think there is a way to do this in a general sense rather than individually

@issueTrack.route('/register')
def register():
    return render_template("register.html")

@issueTrack.route('/roles', methods=['GET', 'POST'])
def roles():
    if request.method == "POST":
        db.execute("UPDATE Users SET Access = ? WHERE Username = ?", (request.form.get("roleselect"), request.form.get("userselect")))
        return redirect('/roles')
    else:
        # Determine access level of current user
        accesslevel = db.execute("SELECT Access FROM Users WHERE Username = ?", (session['user_id'],))
        accesslevel = accesslevel.fetchall()
        accesslevel = accesslevel[0]["Access"]
        useraccess = [{'Username': session['user_id'], 'Access': accesslevel}]
        allowroles = [{'Type': accesslevel}]
        # Determine which users they're allowed to edit
        if accesslevel == "admin":
            # Admin level gets to edit all users
            useraccess = db.execute("SELECT Username, Access FROM Users ORDER BY Access, Username")
            useraccess = useraccess.fetchall()
            # Admin level gets to assign any role to a user
            allowroles = db.execute("SELECT Type FROM Access")
            allowroles = allowroles.fetchall()
        # User level does not get to edit anyone

        return render_template('roles.html', useraccess=useraccess, allowroles=allowroles)

@issueTrack.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@issueTrack.route('/projectusers')
def projectusers():
    return render_template('projectusers.html')

@issueTrack.route('/mytickets')
def mytickets():
    return render_template('mytickets.html')

@issueTrack.route('/myprojects')
def myprojects():
    return render_template('myprojects.html')

@issueTrack.route('/profile')
def profile():
    return render_template('profile.html')
