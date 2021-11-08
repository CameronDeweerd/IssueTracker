from flask import render_template, Blueprint, redirect, request, session, abort, url_for
from jinja2 import TemplateNotFound
from helpers import apology, login_required
from SQLhelpers import execute_query, return_query, check_permission
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
import prepareChartData


issueTrack = Blueprint('issueTrack', __name__, url_prefix='/issue', template_folder='templates',
                          static_folder='static')
# This one will work for local testing
# issueTrack = Blueprint('issueTrack', __name__, url_prefix='/', template_folder='templates', static_folder='static')


# do queries like this:
# var = return_query("SELECT * FROM Access")
# print(var)


@issueTrack.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        # Check if Demo account
        if request.form.get("admin"):
            session["user_id"] = "testadmin"
            return redirect(url_for(".dashboard"))
        elif request.form.get("user"):
            session["user_id"] = "testuser"
            return redirect(url_for(".dashboard"))
        # todo add the other two when they might matter

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")
        # Check database for username
        rows = return_query("SELECT * FROM Users WHERE Username = ?", (request.form.get("username"),))
        # print(rows)
        if len(rows) != 1 or not check_password_hash(rows[0]["Password"], request.form.get("password")):
            return apology("Invalid Username and/or Password")
        # Remember which user has logged in
        session["user_id"] = rows[0]["Username"]

        # Redirect user to home page
        return redirect(url_for(".dashboard"))
    elif session:
        # Redirect user to home page
        return redirect(url_for(".dashboard"))
    else:
        return redirect(url_for(".login"))

@issueTrack.route('/login')
def login():
    return render_template("login.html")


@issueTrack.route('/register', methods=['GET', 'POST'])
def register():
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("usernameEntry"):
            warning = "Please enter username"
            return render_template("register.html", warning=warning)
        # Ensure password was submitted
        if not request.form.get("passwordEntry"):
            warning = "Please enter password"
            return render_template("register.html", warning=warning)
        # Ensure password was confirmed
        if request.form.get("confirmPasswordEntry") != request.form.get("passwordEntry"):
            warning = "Please ensure passwords match"
            return render_template("register.html", warning=warning)
        # Check if username in use
        inuse = return_query("SELECT Username FROM Users WHERE Username = ?", request.form.get("usernameEntry", ))
        if inuse:
            warning = "Username is in use already, please try again"
            return render_template("register.html", warning=warning)
        # If all else is good
        execute_query("INSERT INTO Users (Username, Password, Access) Values (?, ?, ?)", (
        request.form.get("usernameEntry"), generate_password_hash(request.form.get("passwordEntry")), "submitter"))
        return redirect(url_for(".index"))
    else:
        return render_template("register.html")


# will look for a specific route first and if it doesn't find it then it will use this
@issueTrack.route('/<page>')
def show(page):
    try:
        return render_template(f'{page}.html')
    except TemplateNotFound:
        abort(404)


@issueTrack.route('/roles', methods=['GET', 'POST'])
@login_required
def roles():
    if request.method == "POST":
        execute_query("UPDATE Users SET Access = ? WHERE Username = ?",
                      (request.form.get("roleselect"), request.form.get("userselect")))
        return redirect(url_for(".roles"))
    else:
        # TODO change this up to use the SQLhelper function and database permission value
        # Determine access level of current user
        accesslevel = return_query("SELECT Access FROM Users WHERE Username = ?", (session['user_id'],))
        accesslevel = accesslevel[0]["Access"]
        useraccess = [{'Username': session['user_id'], 'Access': accesslevel}]
        allowroles = [{'Type': accesslevel}]
        # Determine which users they're allowed to edit
        if accesslevel == "admin":
            # Admin level gets to edit all users
            useraccess = return_query("SELECT Username, Access FROM Users ORDER BY Access, Username")
            # Admin level gets to assign any role to a user
            allowroles = return_query("SELECT Type FROM Access")
        # User level does not get to edit anyone

        return render_template('roles.html', useraccess=useraccess, allowroles=allowroles)


@issueTrack.route('/logout')
def logout():
    # Forget user_id
    session.clear()
    return redirect(url_for(".login"))


@issueTrack.route('/submitticket', methods=['GET', 'POST'])
@login_required
def submit():
    if request.method == "POST":
        '''form validation'''
        # Ensure category was selected
        if not request.form.get("category"):
            # TODO check values against DB categories
            return apology("invalid category")
        # Ensure subject was submitted
        elif not request.form.get("subject"):
            return apology("Please provide a subject")
        # Ensure description submitted
        elif not request.form.get("description"):
            return apology("Please provide a Description")

        ''' add to DB '''
        query = "INSERT INTO Issues \
                   (issue_category, issue_subject, issue_description, submitter_id, date_created, issue_status) \
                   VALUES (?, ?, ?, ?, ?, 'unassigned')"
        parameters = (request.form.get("category"),
                      request.form.get("subject"),
                      request.form.get("description"),
                      session["user_id"],
                      datetime.now().date())
        execute_query(query, parameters)

        ''' add "created ticket" activity to DB'''
        newTicketID = return_query("SELECT issue_id FROM Issues ORDER BY issue_id DESC LIMIT 1")
        query = "INSERT INTO Activity \
                           (issue_id, user_id, activity_date, activity_description) \
                           VALUES (?, ?, ?, ?)"
        parameters = (newTicketID[0]['issue_id'],
                      session["user_id"],
                      datetime.now().date(),
                      'Ticket Created')
        execute_query(query, parameters)

        return redirect(url_for(".mytickets"))
    else:
        categories = return_query("SELECT category FROM Categories")
        return render_template('submitticket.html', category=categories)


@issueTrack.route('/dashboard')
@login_required
def dashboard():
    # TODO return various different chart data depending on the user access level
    chart1 = prepareChartData.openIssuesByCategory(session["user_id"])
    chart2 = prepareChartData.myTicketStatus(session["user_id"])
    chart3 = prepareChartData.workloadBreakdown()
    return render_template('dashboard.html', chart1JSON=chart1, chart2JSON=chart2, chart3JSON=chart3)


@issueTrack.route('/mytickets', methods=['GET', 'POST'])
@login_required
def mytickets():
    if not request.args.get('id'):

        closed_tickets = return_query("SELECT * FROM Issues WHERE user_assigned_to = ? AND issue_status = 'Closed'", (session['user_id'],))
        # check to see if user has access to all tickets or should just display assigned
        if check_permission('FullAccess'):
            open_tickets = return_query("SELECT * FROM Issues WHERE (user_assigned_to = ? OR issue_status = 'unassigned') AND NOT issue_status = 'Closed'", (session['user_id'],))
        else:
            open_tickets = return_query("SELECT * FROM Issues WHERE user_assigned_to = ? AND NOT issue_status = 'Closed'", (session['user_id'],))
        return render_template('mytickets.html', open_tickets=open_tickets, closed_tickets=closed_tickets)
    else:
        if request.method == "GET":
            '''This will bring us to a specific ticket'''
            # TODO check if user is admin or assigned to ticket
            # TODO check if ticket is actually in the DB
            ticketData = return_query("SELECT * FROM Issues WHERE issue_id = ?", request.args.get('id'))
            activityData = return_query("SELECT * FROM Activity WHERE issue_id = ?", request.args.get('id'))
            activityData.reverse()
            statusOptions = return_query("SELECT * FROM Status")
            return render_template('ticketupdate.html', activityData=activityData, ticketData=ticketData[0],
                                   statusOptions=statusOptions)
        elif request.method == "POST":
            '''This is triggered when activity is submitted on a specific ticket'''
            '''add the new activity into the DB'''
            # TODO check if user has permissions
            description = request.form.get("description")
            status = request.form.get("status")
            if description:  # Update the activity log
                query = "INSERT INTO Activity \
                                   (issue_id, user_id, activity_date, activity_description) \
                                   VALUES (?, ?, ?, ?)"
                parameters = (request.args.get('id'),
                              session["user_id"],
                              datetime.now().date(),
                              request.form.get("description"))
                execute_query(query, parameters)
            if status:  # if the status was changed then update the activity log and issues page
                # Add a new activity
                query = "INSERT INTO Activity \
                                   (issue_id, user_id, activity_date, activity_description) \
                                   VALUES (?, ?, ?, ?)"
                parameters = (request.args.get('id'),
                              session["user_id"],
                              datetime.now().date(),
                              f'Status changed to {status}')
                execute_query(query, parameters)

                # update the issue status
                query = f"UPDATE Issues SET issue_status= ? WHERE issue_id = ?"
                parameters = (status,
                              request.args.get('id'))
                execute_query(query, parameters)

                # include the closing date if needed
                if status == "Closed":
                    query = f"UPDATE Issues SET date_closed = ? WHERE issue_id = ?"
                    parameters = (datetime.now().date(),
                                  request.args.get('id'))
                    execute_query(query, parameters)
            redirectLink = f'{url_for(".mytickets")}?id={request.args.get("id")}'
            print(redirect)
            return redirect(redirectLink)


@issueTrack.route('/assigntickets', methods=['GET', 'POST'])
@login_required
def assigntickets():
    if request.method == "POST":
        issueID = request.form.get("issueID")
        person = request.form.get("people")
        if person:
            execute_query("UPDATE Issues SET user_assigned_to = ?, issue_status = ? WHERE issue_id = ?", (person, "Open", issueID))
            query = ("INSERT INTO Activity \
                    (issue_id, activity_description, user_id, activity_date) VALUES (?, ?, ?, ?)")
            parameters = (issueID, f"Assigned to {person}", session['user_id'], datetime.now().date())
            execute_query(query, parameters)
    if not check_permission('FullAccess'):
        return redirect(url_for(".mytickets"))
    else:
        tickets = return_query("SELECT * FROM Issues WHERE issue_status = ?", ("unassigned",))
        users = return_query("SELECT Username, Access FROM Users")
        return render_template("alltickets.html", tickets=tickets, users=users)


@issueTrack.route('/profile')
def profile():
    username = session['user_id']
    access = return_query("SELECT Access FROM Users WHERE Username = ?", (username,))
    access = access[0]["Access"]
    permissions = return_query("SELECT * FROM Access WHERE Type = ?", (access,))
    permissions = permissions[0]
    permissions.pop("Type")
    return render_template('profile.html', username=username, access=access, permissions=permissions)


@issueTrack.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return apology(e.name, e.code)
    issueTrack.register_error_handler(404, page_not_found)
