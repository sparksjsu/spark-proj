# app/auth/views.py

from flask import request, flash, redirect, render_template, url_for, g
from flask_login import login_required, login_user, logout_user, current_user

from . import auth
#from forms import LoginForm, RegistrationForm
from .. import db
from ..models import Employee
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired
import ldap,re

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle requests to the /login route
    Log an employee in through the login form
    """
    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('home.homepage'))

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')
	email = '%s@xyz.com'%(username)
	print('mahesh: email ' + email)
	employee = Employee.query.filter_by(email = email).first()
	current_employee = employee
	print('employee: ' + employee.email)
	print(employee)
        try:
            print('user={0} passwd={1}'.format(username,password))
            employee.try_login(username, password)
        except ldap.INVALID_CREDENTIALS:
            flash('Invalid username or password. Please try again.', 'danger')
            return render_template('login.html', form=form)

        login_user(employee)
        flash('You have successfully logged in.', 'success')
	ldap_result_id = employee.conn.search("dc=ldap",
	    ldap.SCOPE_SUBTREE,
	    "cn={0}".format(username),
	    ['cn'])
    
	#parse role
	result_type, result_data = employee.conn.result(ldap_result_id, 0)
	if result_data:

	    #check for admin 
	    print(result_data[0][0])
	    m = re.search('admin', result_data[0][0])
	    if m:
		employee.is_admin = True
	    else:
		employee.is_admin = False
	    print('admin: {0}'.format(employee.is_admin))

	    #check for role
	    m = re.search('ou=(.*),', result_data[0][0])
	    if m:
		employee.group = m.group(1)
	    else:
		employee.group = ''
	    print('group: {0}'.format(employee.group))
	else:
	    print('ERROR: unable to parse role')
	db.session.commit()
        return redirect(url_for('home.homepage'))

    if form.errors:
        flash(form.errors, 'danger')

    # load login template
    return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))


#auth = Blueprint('auth', __name__)
#
#
#
@auth.before_request
def get_current_user():
    g.user = current_user

#
#@auth.route('/')
#@auth.route('/home')
#def home():
#    return render_template('home.html')
#

class LoginForm(Form):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
