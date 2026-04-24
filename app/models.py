from mongoengine import Document, StringField, FloatField, IntField, DateTimeField, ReferenceField
from datetime import datetime


class Product(Document):
    name = StringField(required=True)
    description = StringField(required=True)
    price = FloatField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)


class Cart(Document):
    created_at = DateTimeField(default=datetime.utcnow)


class CartItem(Document):
    cart = ReferenceField(Cart, required=True)
    product = ReferenceField(Product, required=True)
    quantity = IntField(default=1)


class Order(Document):
    cart = ReferenceField(Cart, required=True)
    total_amount = FloatField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)


class Payment(Document):
    order = ReferenceField(Order, required=True)
    amount = FloatField(required=True)
    payment_status = StringField(default="success")
    created_at = DateTimeField(default=datetime.utcnow)