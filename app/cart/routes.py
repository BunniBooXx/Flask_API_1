from . import cart 
from flask import request
from flask_jwt_extended import jwt_required, current_user
from ..models import Product, Order, Customer
from ..utils import bad_request_if_none

@cart.post('/new')
@jwt_required()
def handle_create_order():
    body = request.json 

    if body is None: 
        response={
            "message": "invalid request body"
        }
        return response, 400
    order_name = body.get('order_name')
    if order_name is None or order_name =="":
        response = {
            "message": "you need an order name to create a new order"
        }
        return response, 400
    customer_id = body.get('customer_id')
    if customer_id is None or order_name == "": 
        response = {
            "message": "you need a customer id to create an order"
        }
        return response, 400
    

  
   
    
    
   
    
    order = Order(order_name = order_name, customer_id=customer_id)
    order.create()
     
    response = {
        "message": "successfully created product",
        "order":order.to_response()
     }
    
   
    return response, 201

@cart.get("/all")
@jwt_required()
def handle_get_all_order(): 
    orders = Order.query.all()
    response = {
        "message": "products retrieved",
        "products": [order.to_response() for order in orders]
    }
    return response, 200


@cart.get("/order/<order_id>")
@jwt_required()    
def handle_get_one_order(order_id):
    order= Order.query.filter_by(id=order_id).one_or_none()
    if order is None:
        response = {
            "message": "product does not exist"

        }  
        return response, 404  
    
    response = {
        "message": "product found",
        "order": order.to_response()
    }
    return response, 200

@cart.delete('/<order_id>')
@jwt_required()
def handle_delete_product(order_id):
        order= Order.query.filter_by(id=order_id).one_or_none()
        if order is None:
            response = {

                "message": "order does not exist"

            }  
        
            return response, 404 
        order.delete()

        response = {
            "message": f"product {order.id} deleted"

        }
        return response,200

@cart.put('update/<order_id>')
def handle_update_product(order_id): 
    body = request.json

    order= Order.query.filter_by(id=order_id).one_or_none()
    if order is None: 
        response= {
            "message": "not found"
        }
        return response, 404

    order.order_name = body.get('name', order.order_name)
    order.customer_id = body.get('customer_id', order.customer_id)

    
    order.update()

    response ={
        "message": "product updated ",
        "product": order.to_response()
     }
    return response , 200