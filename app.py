from flask import Flask
app = Flask(__name__)

from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
# The . makes these "relative imports" which is important to make them work on the server but technically doesn't matter here.
from .helpers import apology
from .issueTrackerViews import issueTrack

app.register_blueprint(issueTrack)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return apology(e.name, e.code)
app.register_error_handler(404, page_not_found)

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
    app.run()
