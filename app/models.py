from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from random import shuffle

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    created_at= db.Column(db.DateTime, default = datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    username= db.Column(db.String(16), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    orders=db.relationship('Order', backref='customer')

    def __init__(self,username,password):
        self.id= str(uuid4())
        self.username= username
        self.password = generate_password_hash(password)

    def compare_password(self,password):
        return check_password_hash(self.password, password)
    
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self): 
        db.session.delete(self)
        db.session.commit()


    def delete(self): 
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs): 
        for key, value in kwargs.items():
            if key == "password": 
                setattr(self, key, generate_password_hash(value))
            else: 
                setattr(self,key,value)
        db.session.commit()

    
        
    
    def to_response(self):
        return {
            "id": self.id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "username": self.username,
            "orders":[order.to_response() for order in self.orders]
            

        }



order_product= db.Table('order_product', 
    db.Column('order_id', db.String, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.String, db.ForeignKey('product.id'), primary_key=True)
    )
class Order(db.Model): 
    id=db.Column(db.String(64),primary_key=True)
    order_name=db.Column(db.String(64))
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
    updated_at=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    order_date=db.Column(db.DateTime, default=datetime.utcnow)
    shipped_date=db.Column(db.DateTime, default = datetime.utcnow)
    delievered_date=db.Column(db.DateTime, default=datetime.utcnow)
    customer_id=db.Column(db.String(64),db.ForeignKey('customer.id') , nullable=False)
    products=db.relationship('Product', secondary = order_product)


    def __init__(self,customer_id, order_name):
        self.id= str(uuid4())
        self.customer_id= customer_id
        self.order_name = order_name
        

    
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self): 
        db.session.delete(self)
        db.session.commit()


    def delete(self): 
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs): 
        for key, value in kwargs.items():
            setattr(self,key,value)
        db.session.commit()

    def to_response(self):
        return {
            "id":self.id,
            "order_name": self.order_name, 
            "created_at":self.created_at,
            "updated_at":self.updated_at,
            "order_date":self.order_date,
            "shipped_date":self.shipped_date,
            "delievered_date":self.delievered_date,
            "customer_id":self.customer_id,
            "products":[product.to_response() for product in self.products]
        }





class Product(db.Model): 
    id=db.Column(db.String(64), primary_key=True)
    created_at=db.Column(db.DateTime, default = datetime.utcnow)
    updated_at=db.Column(db.DateTime, default= datetime.utcnow, onupdate= datetime.utcnow)
    name= db.Column(db.String(25), unique=True, nullable= False)
    description=db.Column(db.Text)
    price=db.Column(db.Numeric(8,2), nullable=False)
    img_url=db.Column(db.String(300), nullable=False)


    def __init__(self,name,description, price, img_url):
        self.id= str(uuid4())
        self.name= name
        self.description = description
        self.price = price
        self.img_url = img_url

    
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self): 
        db.session.delete(self)
        db.session.commit()


    def delete(self): 
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs): 
        for key, value in kwargs.items():
            setattr(self,key,value)
        db.session.commit()

    def to_response(self):
        return{
            "id": self.id,
            "created_at": self.created_at,
            "updated_at":self.updated_at,
            "name": self.name,
            "description":self.description,
            "price": self.price,
            "img_url":self.img_url
        }