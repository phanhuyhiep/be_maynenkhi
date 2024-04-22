def auth_seriral(auth) -> dict:
    return {
        "id": str(auth["_id"]),
        "name": auth["name"],
        "email": auth["email"],
        "password": auth["password"],
        "password_reset_token": str(auth["password_reset_token"]),
        "role": auth["role"],
    }

def list_auth(auths) -> list:
    return [auth_seriral(auth) for auth in auths]