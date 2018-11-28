from flask_wtf import Form
from wtforms import TextField,StringField, IntegerField, TextAreaField, SubmitField,PasswordField, RadioField,SelectField
from wtforms import validators, ValidationError
from wtforms.widgets import HiddenInput

class ContactForm(Form):
    name = TextField("Name Of Student",[validators.Required("Please enter your name.")])
    Gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
    Address = TextAreaField("Address")
   
    email = TextField("Email",[validators.Required("Please enter your email address."),
      validators.Email("Please enter your email address.")])
   
    Age = IntegerField("age")
    language = SelectField('Languages', choices = [('cpp', 'C++'), 
      ('py', 'Python')])
    submit = SubmitField("Send")

class ContactUpdateForm(Form):
    name = TextField("Name Of Student",[validators.Required("Please enter your name.")])
    
    Gender = TextField('Gender')
    Address = TextAreaField("Address")
   
    email = TextField("Email",[validators.Required("Please enter your email address."),
      validators.Email("Please enter your email address.")])
   
    Age = IntegerField("age")
    language = TextField('Languages')
    submit = SubmitField("Send")


class LoginForm(Form):
    username = TextField("Login Name",[validators.Required("Please enter login name.")])
    password = PasswordField('Password',[validators.Required("Please provide password.")])
    submit = SubmitField("Send")
   