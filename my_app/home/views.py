#app/home/views.py

from flask import render_template
from flask_login import login_required, current_user

from . import home
from .. import db
from ..models import Employee, Customer

@home.route('/')
@login_required
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")

# add employee view
@home.route('/employees')
@login_required
def view_employees():
    # prevent non-admins from accessing the page
    #if not current_user.is_admin:
    #    abort(403)
    employees = Employee.query.all()
    print('mahesh3')
    print(employees)
    print('mahesh3')
    return render_template('home/employees.html', 
	employees=employees, title="Dashboard::Employees")
  
# add customer view
@home.route('/customers')
@login_required
def view_customers():
    global current_employee
    # prevent non-admins from accessing the page
    #if not current_user.is_admin:
    #    abort(403)
    customers = Customer.query.all()
    if  not current_user.is_admin and current_user.group != 'sales':
	return render_template('home/no_permission.html', 
	    title="Dashboard::Permission-Denied")
	
    print(current_user.group)
    print('mahesh3')
    return render_template('home/customers.html', 
	customers=customers, title="Dashboard::Customers")
  
