from flask import Flask
app=Flask(__name__)

from config import Config
app.config.from_object(Config)

from .models import db, Customer
db.init_app(app)

from flask_migrate import Migrate 
migrate = Migrate(app,db)

from flask_jwt_extended import JWTManager
jwt= JWTManager(app)

jwt.user_identity_loader
def user_identity_lookup(customer):
    return customer

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header,jwt_data):
    identity = jwt_data["sub"]
    return Customer.query.filter_by(id=identity).one_or_none()

from .auth import auth_blueprint
app.register_blueprint(auth_blueprint)


from .product import product
app.register_blueprint(product)

from .cart import cart
app.register_blueprint(cart)