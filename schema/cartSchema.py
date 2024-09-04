def cart_serial(cart) -> dict:
    return{
        "id": str(cart["_id"]),
        "nameProduct": str(cart["nameProduct"]),
        "imgProduct": str(cart["imgProduct"]),
        "priceProduct":str(cart["priceProduct"]),
        "quantity":"quantity"
    }
    
def list_cart(carts) -> list:
    return[cart_serial(cart) for cart in carts]