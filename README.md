# E-commerce API Project

This is a beginner-friendly e-commerce REST API built using Flask, SQLAlchemy, Marshmallow, and MySQL.

It allows you to:
- Manage users
- Create and view products
- Create orders and add/remove products from orders

## Technologies Used
- Python
- Flask
- SQLAlchemy
- Marshmallow
- MySQL
- Postman 

---

## How to Set Up the Project

### 1. Clone the repository
Make sure you are in the directory where you want to store the project, then run:

```
git clone <https://github.com/dielac>
```

### 2. Navigate into the project folder
```
cd ecommerce_api_2
```

### 3. Create a virtual environment
```
python3 -m venv venv
```

### 4. Activate the virtual environment
On Mac
```
source venv/bin/activate
```


### 5. Install the dependencies
```
pip install -r requirements.txt
```
If you don't have a requiremtns.tx yet, you can install manually:
```
pip install Flask Flask-SQLAlchemy Flask-Marshmallow marshmallow-sqlalchemy mysql-connector-python
```

### 6. Create the MySQL database
Open MySQL Workbench and run this command:
```
CREATE DATABASE ecommerce_api;
```

### 7. Start the Flask app
Make sure your virtual environment is activated:
```
flask run
```
You should see the message:
```
* Running on http://127.0.0.1:5000
```

---

## API Routes

### Users
- `POST /users` - Create a user
- `GET /users` - Get all users
- `GET /users/<id>` - Get a user by ID
- `PUT /users/<id>` - Update a user by ID
- `DELETE /users/<id>` - Delete a user by ID

### Products
- `POST /products` - Create a product
- `GET /products` - Get all products
- `GET /products/<id>` - Get a product by ID
- `PUT /products/<id>` - Update a product
- `DELETE /products/<id>` - Delete a product

### Orders
- `POST /orders` - Create a new order (needs user ID and order date)
- `PUT /orders/<order_id>/add_product/<product_id>` - Add a product to an order
- `DELETE /orders/<order_id>/remove_product/<product_id>` - Remove a product from an order
- `GET /orders/user/<user_id>` - Get all orders for a user
- `GET /orders/<order_id>/products` - Get all products in an order

---

## Test the API in Postman

