def cart_seriral(cart) -> dict:
    return {
        "id": str(cart["_id"]),
        "product_cart": str(["product_cart"]),
        "quantity": str(["quantity"])
    }

def list_cart(carts) -> list:
    return [cart_seriral(cart) for cart in carts]