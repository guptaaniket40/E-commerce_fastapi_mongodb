from . import models, schemas


def product_to_dict(product):
    return {
        "id": str(product.id),
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "created_at": str(product.created_at)
    }


# PRODUCT CRUD

def get_all_products():
    products = models.Product.objects()
    return [product_to_dict(product) for product in products]


def create_product(product: schemas.ProductCreate):
    new_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price
    )
    new_product.save()
    return product_to_dict(new_product)


def get_product_by_id(product_id: str):
    product = models.Product.objects(id=product_id).first()
    if not product:
        return None
    return product_to_dict(product)


def update_product(product_id: str, product: schemas.ProductCreate):
    existing_product = models.Product.objects(id=product_id).first()

    if not existing_product:
        return None

    existing_product.name = product.name
    existing_product.description = product.description
    existing_product.price = product.price
    existing_product.save()

    return product_to_dict(existing_product)


def delete_product(product_id: str):
    product = models.Product.objects(id=product_id).first()

    if not product:
        return None

    product.delete()
    return True


# CART

def create_cart():
    cart = models.Cart()
    cart.save()

    return {
        "cart_id": str(cart.id),
        "message": "Cart created successfully"
    }


def add_to_cart(data: schemas.AddToCartSchema):
    cart = models.Cart.objects(id=data.cart_id).first()
    product = models.Product.objects(id=data.product_id).first()

    if not cart or not product:
        return None, "Cart or Product not found"

    item = models.CartItem.objects(
        cart=cart,
        product=product
    ).first()

    if item:
        item.quantity += data.quantity
        item.save()
    else:
        item = models.CartItem(
            cart=cart,
            product=product,
            quantity=data.quantity
        )
        item.save()

    return {
        "item_id": str(item.id),
        "product_id": str(product.id),
        "quantity": item.quantity
    }, None


def view_cart(cart_id: str):
    cart = models.Cart.objects(id=cart_id).first()

    if not cart:
        return None

    items = models.CartItem.objects(cart=cart)

    data = []

    for item in items:
        data.append({
            "item_id": str(item.id),
            "product_id": str(item.product.id),
            "product_name": item.product.name,
            "product_price": item.product.price,
            "quantity": item.quantity
        })

    return {
        "cart_id": str(cart.id),
        "items": data
    }


def remove_from_cart(item_id: str):
    item = models.CartItem.objects(id=item_id).first()

    if not item:
        return None

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
        return "Quantity decreased"

    item.delete()
    return "Item removed"


# CHECKOUT

def checkout(cart_id: str):
    cart = models.Cart.objects(id=cart_id).first()

    if not cart:
        return None, "Cart not found"

    items = models.CartItem.objects(cart=cart)

    if not items:
        return None, "Cart is empty"

    total = 0

    for item in items:
        total += item.product.price * item.quantity

    order = models.Order(
        cart=cart,
        total_amount=total
    )
    order.save()

    payment = models.Payment(
        order=order,
        amount=total,
        payment_status="success"
    )
    payment.save()

    return {
        "order_id": str(order.id),
        "total": total,
        "payment": "success"
    }, None