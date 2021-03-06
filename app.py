from flask import Flask, session
from flask_session import Session
from tempfile import mkdtemp
app = Flask(__name__)

from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
# The . makes these "relative imports" which is important to make them work on the server but technically doesn't matter here.
from issueTrackerViews import issueTrack

app.register_blueprint(issueTrack)

# todo doublecheck that all things wrt filesystem don't cause problems
# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Some of these leading sections were taken directly from CS50's PSET9 source code
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True
Session(app)

'''This needs to be checked but it should in theory catch the non-404 errors'''
# def errorhandler(e):
#     pass
#     """Handle error"""
#     if not isinstance(e, HTTPException):
#         e = InternalServerError()
#     return apology(e.name, e.code)
#
#
# #Listen for errors
# for code in default_exceptions:
#     app.errorhandler(code)(errorhandler)


if __name__ == '__main__':
    app.run(debug=True)
