import ldap
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from my_app import db, login_manager

class Office(db.Model):


    """create offices table """

    __tablename__ = 'offices'


    officeCode = db.Column(db.String(10), primary_key=True)
    city = db.Column(db.String(50), nullable = False)
    phone = db.Column(db.String(50), nullable = False)
    addressLine1 = db.Column(db.String(50), nullable = False)
    addressLine2 = db.Column(db.String(50))
    state = db.Column(db.String(50))
    country = db.Column(db.String(50), nullable = False)
    postalCode = db.Column(db.String(50), nullable = False)
    territory = db.Column(db.String(10), nullable = False)




class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    employeeNumber = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), nullable = False)
    last_name = db.Column(db.String(60), nullable = False)
    extension = db.Column(db.String(10))
    email = db.Column(db.String(100), nullable = False)
    jobTitle = db.Column(db.String(50), nullable = False)
    reportsTo = db.Column(db.String(50))
    officeCode = db.Column(db.String(10), db.ForeignKey('offices.officeCode'))
    is_admin = db.Column(db.Integer)
    group = db.Column(db.String(10))

    username = None
    conn = None
    def __init__(self, username, password):
        self.username = username

    def get_ldap_connection(self):
	self.conn = ldap.initialize('ldap://ldap')

    def try_login(self, username, password):
        self.get_ldap_connection()
        self.conn.simple_bind_s(
            'cn=admin,dc=ldap', password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.employeeNumber)

class Customer(db.Model):

    """create customers table """
    
    __tablename__ = 'customers'

    
    customerNumber = db.Column(db.Integer, primary_key=True)
    customerName = db.Column(db.String(50), nullable = False)
    contactLastName = db.Column(db.String(50), nullable = False)
    contactFirstName = db.Column(db.String(50), nullable = False)
    phone = db.Column(db.String(50), nullable = False)
    addressLine1 = db.Column(db.String(50), nullable = False)
    addressLine2 = db.Column(db.String(50))
    city = db.Column(db.String(50), nullable = False)
    state = db.Column(db.String(50), nullable = False)
    postalCode = db.Column(db.String(50))
    country = db.Column(db.String(50), nullable = False)
    salesRepEmployeeNumber = db.Column(db.Integer, db.ForeignKey('employees.employeeNumber'))



class Productlines(db.Model):


    """create productlines table """

    __tablename__ = 'productlines'


    productline = db.Column(db.String(50), primary_key=True)
    textDescription = db.Column(db.String(500))
    htmlDescription = db.Column(db.String(50))
    image = db.Column(db.String(50))


class Product(db.Model):

    """create products table """

    __tablename__ = 'products'


    productCode = db.Column(db.String(15), primary_key=True)
    productName = db.Column(db.String(70), nullable = False)
    productLine = db.Column(db.String(50), nullable = False)
    productScale = db.Column(db.String(10), nullable = False)
    productVendor = db.Column(db.String(50), nullable = False)
    productDescription = db.Column(db.String(50), nullable = False)
    quantityInStock = db.Column(db.Integer, nullable = False)
    buyPrice = db.Column(db.Float, nullable = False)
    MSRP = db.Column(db.Float, nullable = False)
   

class Payment(db.Model):


    """create payment table """

    __tablename__ = 'payments'

    
    customerNumber = db.Column(db.Integer, primary_key = True)
    checkNumber = db.Column(db.String(50), nullable = False)
    paymentDate = db.Column(db.DateTime, nullable = False)
    amount = db.Column(db.Float, nullable = False)


class Orderdetails(db.Model):

    """create orderdetails table """

    __tablename__ = 'orderdetails'


    orderNumber = db.Column(db.Integer, primary_key=True)
    productCode = db.Column(db.String(15), db.ForeignKey('products.productCode'))
    quantityOrdered = db.Column(db.Float, nullable = True)
    priceEach = db.Column(db.Float, nullable = False)
    orderLineNumber = db.Column(db.Integer, nullable = False)

class Order(db.Model):

    """create order table """

    __tablename__ = 'orders'


    orderNumber = db.Column(db.Integer, primary_key=True)
    orderDate= db.Column(db.String(15), nullable = True)
    requiredDate = db.Column(db.String(15), nullable = True)
    status = db.Column(db.String(15), nullable = True)
    comments = db.Column(db.String(100), nullable = True)
    customerNumbers = db.Column(db.Integer, nullable = False)

@login_manager.user_loader
def load_user(id):
    return Employee.query.get(int(id))
