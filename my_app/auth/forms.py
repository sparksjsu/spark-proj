#app/auth/forms.py

from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import Employee

class RegistrationForm(FlaskForm):
    """
    Form for employees to create new account
    """
    employeeNumber = IntegerField('employeeNumber', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    extension = StringField('extension')
    email = StringField('Email', validators=[DataRequired(), Email()])
    jobTitle = StringField('jobTitle', validators=[DataRequired()])
    officeCode = StringField('officeCode', validators=[DataRequired()])
    reportsTo = StringField('reportsTo')

    submit = SubmitField('Register')

    def validate_email(self, field):
        if Employee.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use.')

    def validate_username(self, field):
        if Employee.query.filter_by(employeeNumber=field.data).first():
            raise ValidationError('Employee is already in use.')

class LoginForm(FlaskForm):
    """
    Form for employee to login
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    employeeNumber = StringField('employeeNumber', validators=[DataRequired()])
    submit = SubmitField('Login')


