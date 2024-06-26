def category_serial(category) -> dict:
    return {
        "id": str(category["_id"]),
        "name": category["name"]
    }
    
def list_category(categorys) -> list:
    return [category_serial(category) for category in categorys]