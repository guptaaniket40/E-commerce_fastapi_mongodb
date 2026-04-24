from fastapi import APIRouter, HTTPException
from .. import schemas, crud

router = APIRouter()


# PRODUCT CRUD

@router.get("/products/", response_model=list[schemas.ProductResponse])
def get_products():
    return crud.get_all_products()


@router.post("/products/", response_model=schemas.ProductResponse)
def create_product(product: schemas.ProductCreate):
    return crud.create_product(product)


@router.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: str):
    product = crud.get_product_by_id(product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: str, product: schemas.ProductCreate):
    updated_product = crud.update_product(product_id, product)

    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")

    return updated_product


@router.delete("/products/{product_id}")
def delete_product(product_id: str):
    deleted_product = crud.delete_product(product_id)

    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted successfully"}


# CART

@router.post("/cart/create")
def create_cart():
    return crud.create_cart()


@router.post("/cart/add")
def add_to_cart(data: schemas.AddToCartSchema):
    item, error = crud.add_to_cart(data)

    if error:
        raise HTTPException(status_code=404, detail=error)

    return {
        "message": "Product added to cart",
        "item": item
    }


@router.get("/cart/view/{cart_id}", response_model=schemas.CartResponse)
def view_cart(cart_id: str):
    cart = crud.view_cart(cart_id)

    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    return cart


@router.delete("/cart/remove/{item_id}")
def remove_from_cart(item_id: str):
    result = crud.remove_from_cart(item_id)

    if not result:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": result}


# CHECKOUT

@router.post("/checkout/{cart_id}", response_model=schemas.OrderResponse)
def checkout(cart_id: str):
    result, error = crud.checkout(cart_id)

    if error:
        raise HTTPException(status_code=400, detail=error)

    return result