def product_serial(product) -> dict:
    return{
        "id": str(product["_id"]),
        "name": product["name"],
        "price": product["price"],
        "quantity": product["quantity"],
        "description": product["description"],
        "categoryId": product["categoryId"]
    }
def list_product(products) -> list:
    return [product_serial(product) for product in products]
    