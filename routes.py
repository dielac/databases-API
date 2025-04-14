from flask import request, jsonify
from app import app, db
from models import Customer, Orders, Products, order_products
from schemas import customer_schema, customers_schema, product_schema, products_schema, order_schema, orders_schema
from marshmallow import ValidationError
from sqlalchemy import select
from datetime import datetime



# ------------------- Home Route -------------------
@app.route("/", methods=["GET"])
def home():
    return "Welcome to the E-commerce API!"  # what shows up on the browser page 



# ------------------- Customer Routes -------------------

# creating a new user
@app.route("/users", methods=["POST"])
def create_user():
    try:
        print("Request JSON:", request.json)  #  debugging
        data = customer_schema.load(request.json)  
    except ValidationError as err:
        print("Validation Error:", err.messages)  # bad input 
        return jsonify(err.messages), 400

    new_user = data  # already a Customer instance
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created", "user": customer_schema.dump(new_user)}), 201



# get all users
@app.route("/users", methods=["GET"])
def get_users():
    users = db.session.execute(select(Customer)).scalars().all()
    return customers_schema.jsonify(users)



# get a single user by ID
@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = db.session.get(Customer, id)
    if user:
        return customer_schema.jsonify(user)
    return jsonify({"message": "User not found"}), 404



# update a user
@app.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    user = db.session.get(Customer, id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    try:
        data = customer_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in data.items():  # loop through fields and update each
        setattr(user, key, value)

    db.session.commit()
    return jsonify({"message": "User updated", "user": customer_schema.dump(user)})



# delete a user
@app.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = db.session.get(Customer, id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"})




# ------------------- ----------------Product Routes -------------------

# create a product
@app.route("/products", methods=["POST"])
def create_product():
    try:
        data = product_schema.load(request.json)  # validate product
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_product = data  # already a Product 
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product created", "product": product_schema.dump(new_product)}), 201


# get all products
@app.route("/products", methods=["GET"])
def get_products():
    products = db.session.execute(select(Products)).scalars().all()
    return products_schema.jsonify(products)


# get one product by id
@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = db.session.get(Products, id)
    if product:
        return product_schema.jsonify(product)
    return jsonify({"message": "Product not found"}), 404


# update a product
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = db.session.get(Products, id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    try:
        data = product_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in data.items():
        setattr(product, key, value)

    db.session.commit()
    return jsonify({"message": "Product updated", "product": product_schema.dump(product)})


# delete a product
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = db.session.get(Products, id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted"})


# ------------------- Order Routes --------------------------------------------------------

# create an order ( attach products after)
@app.route("/orders", methods=["POST"])
def create_order():
    try:
        print("RAW JSON FROM REQUEST:", request.json)  # debugging
        data = order_schema.load(request.json)  # validate order
        print("LOADED DATA FROM SCHEMA:", data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    customer = db.session.get(Customer, data.customer_id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 400

    try:
        order_date = datetime.strptime(str(data.order_date), "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"message": "Invalid date format. Use YYYY-MM-DD."}), 400

    new_order = data
    db.session.add(new_order)
    db.session.commit()

    return jsonify({"Message": "New Order Placed!", "order": order_schema.dump(new_order)}), 201


# add a product to an order
@app.route("/orders/<int:order_id>/add_product/<int:product_id>", methods=["PUT"])
def add_product_to_order(order_id, product_id):
    order = db.session.get(Orders, order_id)
    product = db.session.get(Products, product_id)

    if order and product:
        if product not in order.products:
            order.products.append(product)
            db.session.commit()
            return jsonify({"Message": "Successfully added product to order."})
        else:
            return jsonify({"Message": "Product already in order."}), 400

    return jsonify({"Message": "Invalid order or product ID."}), 400


# remove a product from an order
@app.route("/orders/<int:order_id>/remove_product/<int:product_id>", methods=["DELETE"])
def remove_product_from_order(order_id, product_id):
    order = db.session.get(Orders, order_id)
    product = db.session.get(Products, product_id)

    if order and product:
        if product in order.products:
            order.products.remove(product)
            db.session.commit()
            return jsonify({"Message": "Product removed from order."})
        return jsonify({"Message": "Product not in order."}), 404

    return jsonify({"Message": "Invalid order or product ID."}), 400


# get all orders for a certain user
@app.route("/orders/user/<int:customer_id>", methods=["GET"])
def get_orders_for_user(customer_id):
    customer = db.session.get(Customer, customer_id)
    if not customer:
        return jsonify({"Message": "Customer not found"}), 404

    return orders_schema.jsonify(customer.orders)


# get all products in a certain order
@app.route("/orders/<int:order_id>/products", methods=["GET"])
def get_products_for_order(order_id):
    order = db.session.get(Orders, order_id)
    if not order:
        return jsonify({"Message": "Order not found"}), 404

    return products_schema.jsonify(order.products)