def cart_serial(cart) -> dict:
    return{
        "id": str(cart["_id"]),
        "quantity": cart["quantity"],
        "productId":cart["productId"]
    }
    
def list_cart(carts) -> list:
    return[cart_serial(cart) for cart in carts]