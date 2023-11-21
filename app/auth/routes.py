from . import auth_blueprint as auth
from flask_login import  login_user, login_required,current_user
from werkzeug.security import generate_password_hash
from flask import request, make_response, render_template
from ..models import Customer
from datetime import timedelta 




@auth.route('/')
def index():
    return render_template('index.html')


@auth.post('/register')
def handle_register(): 
    body = request.json

    if body is None: 
        response = {
            "message": "username and password are required to register"

        }
        return response, 400
    username = body.get("username")
    if username is None: 
        response = {
            "message": "username is required"
        }
        return response , 400
    

    existing_user = Customer.query.filter_by(username=username).one_or_none()
    if existing_user is not None: 
        response={
            "message": "username already in use"
        }
        return response, 400
    
    password = body.get("password")
    if password is None: 
        response = {
            "message": "password is required"
        }
        return response , 400
    
    customer = Customer(username=username, password=password)
    customer.create()

    response={
        "message": "user registered",
        "data": customer.to_response()

    } 

    return response, 201

@auth.post("/login")
def handle_login(): 
    body = request.json

    if body is None: 
        response = {
            "message": "username and password are required to login"
        }
        return response,400
    
    username=body.get("username")
    if username is None:
        response = {
            "message": "username is required"
        }
        return response, 400
    
    password = body.get("password")
    if password is None: 
        response = {
            "message": "password is required"
        }
        return response, 400

    customer = Customer.query.filter_by(username=username).one_or_none()
    if customer is None: 
        response = {
            "message": "please create an account before trying to login"
        }
        return response, 400
    
    ok = customer.compare_password(password)
    if not ok:
        response={
            "message": "invalid login"

        }
        return response, 401
    login_user(customer)
    
    response = {
        "message": "successfully logged in"
    }

    return response , 200


    


from flask_login import login_required, current_user

@auth.put('/update-profile')
@login_required
def update_profile():
    customer = current_user  # Use Flask-Login's current_user

    # Get data from the request JSON
    body = request.json
    new_username = body.get("new_username")
    new_password = body.get("new_password")

    # Update username if provided
    if new_username is not None:
        customer.username = new_username

    # Update password if provided
    if new_password is not None:
        hashed_password = generate_password_hash(new_password)
        customer.password = hashed_password

    # Save changes to the database
    customer.save()

    response = {
        "success": True,
        "message": "Profile updated successfully",
        "data": customer.to_response() 
    }

    return response, 200


@auth.delete('/delete-account')
@login_required
def delete_account():
    try:
        # Get the current user's identity from the JWT
        current_user_id = current_user.get_id()

        # Query the database to get the customer object
        customer = Customer.query.get(current_user_id)

        # Delete the customer account
        customer.delete()

        # Create a response
        response = {
            "message": "Account deleted successfully",
        }

        return response, 200

    except Exception as e:
        # Handle exceptions, log errors, etc.
        print(f"Error deleting account: {str(e)}")
        response = {
            "message": "An error occurred while deleting the account",
        }
        return response, 500




