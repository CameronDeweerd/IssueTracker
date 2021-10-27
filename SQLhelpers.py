"""All SQL related helper functions to be kept here"""
import sqlite3
from flask import session   # TODO make it so i don't need this import here


def SQL_connect():
    # Connect to database todo don't know if checksamethread=false is bad practice
    connection = sqlite3.connect("./static/IssueTracker.db", check_same_thread=False)
    connection.row_factory = dict_factory
    return connection


# This function helps convert list of tuple output of sql query into list of dictionaries output
# Taken from https://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Helper function for SQL execution when returns are unneeded
def execute_query(query, options=[]):
    connection = SQL_connect()
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
    connection.close()


# Helper function for SQL execution when returns are needed
def return_query(query, options=[]):
    connection = SQL_connect()
    cursor = connection.cursor()
    try:
        if len(options) == 0:
            result = cursor.execute(query)
        else:
            result = cursor.execute(query, options)
        result = result.fetchall()
        return result
    except Exception as err:
        print(f"Error: '{err}'")
    cursor.close()
    connection.close()


def check_permission(permission):
    value = return_query("SELECT * FROM Access WHERE Type = (SELECT Access FROM Users WHERE Username = ?)", (session['user_id'],))
    # value = value.fetchall()[0]
    return value[0][permission] == 1
