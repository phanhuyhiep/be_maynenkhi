def product_serial(product) -> dict:
    return {
        "id": str(product.get("_id", "N/A")),
        "name": product.get("name", "N/A"),
        "images": product.get("images", ["N/A"]),
        "price": product.get("price", "N/A"),
        "quantity": product.get("quantity", "N/A"),
        "description": product.get("description", "N/A"),
        "categoryName": product.get("categoryName", "N/A")
    }
def list_product(products) -> list:
    return [product_serial(product) for product in products]
    