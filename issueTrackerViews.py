from flask import render_template, Blueprint, redirect, request, session
from flask_session import Session
from tempfile import mkdtemp
from helpers import login_required



issueTrack = Blueprint('issueTrack', __name__, url_prefix='/issue', template_folder='templates')


@issueTrack.route('/')
def index():
    return render_template("login.html")

@issueTrack.route('/register')
def register():
    return render_template("register.html")
