from flask import Flask, request, redirect, render_template
import cgi
import os


app = Flask(__name__)
app.config['DEBUG'] = True

# this creates route to display the form
@app.route('/signup')
def display_user_signup_form():
    return render_template('user-signup-form.html')

#this are functions for the validations

def empty_val(x):
    if x:
        return True
    else:
        return False

def char_length(x):
    if len(x)>2 and len(x)<21:
        return True 
    else:
        return False     

def email_at_symbol(x):
    if x.count('@') >= 1:
        return True 
    else:
        return False  

def email_at_symbol_more_than_one(x):
    if x.count('@') <= 1:
        return True 
    else:
        return False  

def email_period(x):
    if x.count('.') >= 1:
        return True 
    else:
        return False     

def email_period_more_than_one(x):
    if x.count('.') <= 1:
        return True 
    else:
        return False                                        

#this creates route to process and validate the form
@app.route("/signup", methods=['POST'])
def user_signup_complete():

#this creates variables from the form inputs
    username = request.form["username"]
    password = request.form["password"]
    password_validate = request.form["password_validate"]
    email = request.form["email"]

#this creates empty strings for the error messages 
    username_error = ''
    password_error = ''
    password_validate_error = ''
    email_error = ''

#these are the error messages that occur more than once
    err_required ="Required field"
    err_reenter_pw ="Please re-enter password"
    err_char_count="must be between 3 and 20 characters"
    err_no_spaces="must not contain spaces"

# this is for password validation

    if not empty_val(password):
        password_error = err_required
        password = ''
        password_validate = ''
    elif not char_length(password):
        password_error = "Password"  + err_char_count
        password = ''
        password_validate = ''
        password_validate_error = err_reenter_pw
    else:
        if " " in password:
            password_error = "Password" + err_no_spaces
            password = ''
            password_validate = ''
            password_validate_error = err_reenter_pw

# THIS IS THE SECOND PASSWORD VALIDATION   
    if password_validate != password: 
       password_validate_error = "Passwords must match"
       password = ''
       password_validate = ''
       password_error = "Passwords must match"

# THIS IS FOR USERNAME VALIDATION

    if not empty_val(username):
        username_error = err_required
        password = ''
        password_validate = ''
        password_error = err_reenter_pw
        password_validate_error = err_reenter_pw
    elif not char_length(username):
        username_error = "Username"  + err_char_count
        password = ''
        password_validate = ''
        password_error = err_reenter_pw
        password_validate_error = err_reenter_pw
    else:
        if " " in username:
            password_error = "Username" + err_no_spaces
            password = ''
            password_validate = ''
            password_error = err_reenter_pw
            password_validate_error = err_reenter_pw     

# this is the email validation

# checks to see if email contains text prior to running validations
    if email_val(email):
    # validation starts from here
        """
        if not char_length(email):
            email_error = "Email"  + err_char_count
            password = ''
            password_validate = ''
            password_error = err_reenter_pw
            password_validate_error = err_reenter_pw
        el"""
        if not email_at_symbol(email):
            email_error = "Email must contain the @ symbol"
            password = ''
            password_validate = ''
            password_error = err_reenter_pw
            password_validate_error = err_reenter_pw
        elif not email_at_symbol_more_than_one(email):
            email_error = "Email must contain only one @ symbol"
            password = ''
            password_validate = ''
            password_validate_error = err_reenter_pw
        elif not email_period(email): 
            email_error = "Email must contain . "
            password = ''
            password_validate = ''
            password_error = err_reenter_pw
            password_validate_error = err_reenter_pw 
        elif not email_period_more_than_one(email): 
            email_error = "Email must contain only one . "
            password = ''
            password_validate = ''
            password_error = err_reenter_pw
            password_validate_error = err_reenter_pw 
        else:
            if " " in email:
                password_error = "Email" + err_no_spaces
                password = ''
                password_validate = ''
                password_error = err_reenter_pw
                password_validate_error = err_reenter_pw          

# if there are no errors, this will redirect to welcome.html
# if there are errors, this will stay on user-signup-form.html and display the error messages             
    
    if not username_error and not password_error and not password_validate_error and not email_error:
        username = username
        return redirect('/welcome?username={0}'.format(username))

    #Returns to user-signup-form if any conditions are not met
    else:
        return render_template('user-signup-form.html', username_error=username_error, username=username, password_error=password_error, password=password, 
        password_validate_error=password_validate_error,password_validate=password_validate, email_error=email_error,email=email)
        

#this redirects to a welcome page
@app.route('/welcome')
def valid_signup():
    username = request.args.get('username')
    return render_template('welcome.html', username=username)

app.run()