#app/admin/views.py

from flask import render_template
from flask_login import login_required

#from . import home
from . import admin


#@home.route('/')
@admin.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")

