from flask import Flask
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/auth/*": {"origins": "*"}})



from config import Config
app.config.from_object(Config)

from .models import db
db.init_app(app)

from flask_migrate import Migrate
migrate = Migrate(app, db)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

from .auth import auth_blueprint
app.register_blueprint(auth_blueprint)

from .product import product
app.register_blueprint(product)

from .cart import cart
app.register_blueprint(cart)
