#app/home/views.py

from flask import render_template, request
from flask_login import login_required, current_user

from . import home
from .. import db
from ..models import Employee, Customer, Office, Order, Orderdetails, Product, Payment

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
    if  not current_user.is_admin and current_user.group != 'sales':
	return render_template('home/no_permission.html', 
	    title="Dashboard::Permission-Denied")
	
    customers = Customer.query.all()
    return render_template('home/customers.html', 
	customers=customers, title="Dashboard::Customers")
  
# add product view
@home.route('/products')
@login_required
def view_products():
    products = Product.query.all()
    return render_template('home/products.html', 
	products=products, title="Dashboard::Products")
  
# add office view
@home.route('/offices')
@login_required
def view_offices():
    offices = Office.query.all()
    return render_template('home/offices.html', 
	offices=offices, title="Dashboard::Offices")
  
# add oerder view
@home.route('/orders')
@login_required
def view_orders():
    global current_employee
    if (not current_user.is_admin and 
	current_user.group != 'finance' and
	current_user.group != 'sales') :
	return render_template('home/no_permission.html', 
	    title="Dashboard::Permission-Denied")

    orders = Order.query.all()
    return render_template('home/orders.html', 
	orders=orders, title="Dashboard::Orders")
  
# add oerder view 
@home.route('/orderDetails')
@login_required
def view_order_details():
    global current_employee
    if (not current_user.is_admin and 
	current_user.group != 'finance' and
	current_user.group != 'sales') :
	return render_template('home/no_permission.html', 
	    title="Dashboard::Permission-Denied")

    orderNumber = int(request.args.get('orderNumber'))
    print(orderNumber)
    orderdetails = Orderdetails.query.get(orderNumber)
    print(orderdetails)
    return render_template('home/order_details.html', 
	orderdetails=orderdetails, title="Dashboard::Order Details %d"%(orderNumber))

# add payment view
@home.route('/payments')
@login_required
def view_payments():
    global current_employee
    if (not current_user.is_admin and 
	current_user.group != 'finance' and
	current_user.group != 'sales') :
	return render_template('home/no_permission.html', 
	    title="Dashboard::Permission-Denied")

    payments = Payment.query.all()
    return render_template('home/payments.html', 
	payments=payments, title="Dashboard::Payments")
  
