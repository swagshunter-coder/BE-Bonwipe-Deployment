from sqlalchemy import Column, Integer,  String, Float,  ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    
    products = relationship('Product', back_populates='category')
    
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    image_url = Column(String(255))
    stock = Column(Integer, nullable=False, default=0) 
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="products")
    
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    customer_email = Column(String(100), nullable=True)
    customer_phone = Column(String(20), nullable=False)
    shipping_address = Column(Text, nullable=False)
    transfer_proof = Column(String(255))
    status = Column(String(50), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    bank_id = Column(Integer, ForeignKey("banks.id"))
    bank = relationship("Bank", back_populates="orders")

    items = relationship("OrderItem", back_populates="order")

    
class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    price_at_order = Column(Float, nullable=False) 

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

class Bank(Base):
    __tablename__ = "banks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    account_number = Column(String(50), nullable=False)

    orders = relationship("Order", back_populates="bank")
