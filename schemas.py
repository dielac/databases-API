from flask_marshmallow import Marshmallow
from models import Customer, Orders, Products


ma = Marshmallow()




# -------------------------------- Customer Schema -------------------

# This is the validation for the customer model
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        load_instance = True  # this tells Marshmallow to return model 




# ------------------- Product Schema ------------------------------------------

# this handles products (name, price, etc.)
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Products
        load_instance = True




# -------------------- Order Schema ---------------------------------------

# This has the customer id key 
# handles orders
class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Orders
        include_fk = True  # tells Marshmallow to include foreign keys / customer_id
        load_instance = True




# ----------------------- Schema Instances -----------------------



customer_schema = CustomerSchema()            #  single user
customers_schema = CustomerSchema(many=True)  #  a list of users

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
