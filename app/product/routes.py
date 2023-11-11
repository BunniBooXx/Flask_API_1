from . import product 
from flask import request
from flask_jwt_extended import jwt_required, current_user
from ..models import Product, Order, Customer
from ..utils import bad_request_if_none

@product.post('/new')
@jwt_required()
def handle_create_product():
    body = request.json 

    if body is None: 
        response={
            "message": "invalid request body"
        }
        return response, 400
    
    name = body.get('name')
    if name is None or name =="":
        response = {
            "message": "invalid request"
        }
        return response, 400

    description = body.get('description')
    if description is None or description =="":
        response = {
            "message": "invalid request"
        }
        return response, 400
    

    price = body.get('price')
    if price is None or price =="":
        response = {
            "message": "invalid request"
        }

    existing_product = Product.query.filter_by(name=name).one_or_none()
    if existing_product  is not None:
        response = {
            "message": "that name is already in use"
        }
        return response, 400
    
    img_url = body.get('img_url')
    if img_url is None or img_url =="":
        response = {
            "message": "you need an image url to complete the form"
        }
        return response, 400

    product = Product(name=name, description=description,price=price, img_url=img_url)
    product.create()
     
    response = {
        "message": "successfully created product",
        "product":product.to_response()
     }
    
   
    return response, 201

@product.get("/all")
@jwt_required()
def handle_get_all_product(): 
    products = Product.query.all()
    response = {
        "message": "products retrieved",
        "products": [product.to_response() for product in products]
    }
    return response, 200


@product.get("/<product_id>")
@jwt_required()    
def handle_get_one_product(product_id):
    product = Product.query.filter_by(id=product_id).one_or_none()
    if product is None:
        response = {
            "message": "product does not exist"

        }  
        return response, 404  
    
    response = {
        "message": "product found",
        "product": product.to_response()
    }
    return response, 200

@product.delete('/<product_id>')
@jwt_required()
def handle_delete_product(product_id):
        product = Product.query.filter_by(id=product_id).one_or_none()
        if product is None:
            response = {

                "message": "product does not exist"

            }  
        
            return response, 404 
        product.delete()

        response = {
            "message": f"product {product.id} deleted"

        }
        return response,200

@product.put('update/product/<product_id>')
def handle_update_product(product_id): 
    body = request.json

    product= Product.query.filter_by(id=product_id).one_or_none()
    if product is None: 
        response= {
            "message": "not found"
        }
        return response, 404

    product.name = body.get('name', product.name)
    product.description = body.get('description', product.description)
    product.price = body.get('price', product.price)
    product.img_url= body.get('img_url', product.img_url)
    
    product.update()

    response ={
        "message": "product updated ",
        "product": product.to_response()
     }
    return response , 200

