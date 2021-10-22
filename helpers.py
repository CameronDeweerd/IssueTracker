# import os
# import requests
# import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


# This function helps convert list of tuple output of sql query into list of dictionaries output
# Taken from https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Helper function for SQL execution when returns are needed
def return_query(connection, query, options=[]):
    cursor = connection.cursor()
    try:
        if len(options) == 0:
            result = cursor.execute(query)
        else:
            result = cursor.execute(query, options)
        return result
    except Exception as err:
        print(f"Error: '{err}'")
    cursor.close()


# Helper function for SQL execution when returns are unneeded
def execute_query(connection, query, options=[]):
    cursor = connection.cursor()
    try:
        if len(options) == 0:
            cursor.execute(query)
        else:
            cursor.execute(query, options)
        connection.commit()
        # print("Query successful")
    except Exception as err:
        print(f"Error: '{err}'")
    cursor.close()
