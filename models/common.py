def paginate_response(data, page: int, total_items: int, limit: int, total_pages: int):
    return {
        "listResponse": data,
        "page": page,
        "total_items": total_items,
        "total_pages": total_pages,
        "limit": limit,
    }

def message_response(message: str):
    return {
        "message": message,
    }