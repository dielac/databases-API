from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Integer, String, Float, Date
from typing import List




# ------------------- Base Setup -------------------

# create a base class to get things from
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


# ------------------- Association Table -------------------

# many-to-many relations between orders and products
# below is the link table that connects them
order_products = Table(
    'order_products',
    Base.metadata,
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)


# ------------------- Customer (User) -------------------

class Customer(Base):
    __tablename__ = 'Customer'  #  capitalized name/ you dont have to 

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(100), unique=True)

    # one customer can have many orders
    orders: Mapped[List['Orders']] = relationship("Orders", back_populates="customer")




# ------------------- Orders -------------------

class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_date: Mapped[Date] = mapped_column(Date, nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey('Customer.id'))

    # link back to the customer who placed the order
    customer: Mapped['Customer'] = relationship("Customer", back_populates="orders")

    # one order can have many products (and vice versa)
    products: Mapped[List['Products']] = relationship("Products", secondary=order_products, back_populates="orders")




# ------------------- Products -------------------

class Products(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    # one product can appear in many orders
    orders: Mapped[List['Orders']] = relationship("Orders", secondary=order_products, back_populates="products")
