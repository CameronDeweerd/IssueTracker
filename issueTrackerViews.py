from flask import render_template, Blueprint
from webApp import app


issueTrack = Blueprint('issueTrack', __name__, url_prefix='/issue', template_folder='templates')


@issueTrack.route('/')
def index2():
    return render_template("index2.html")
