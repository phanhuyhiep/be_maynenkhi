from fastapi import FastAPI

from routes.category import router_category
from routes.product import router_product
from routes.auth import router_auth

app = FastAPI()

app.include_router(router_category)
app.include_router(router_product)
app.include_router(router_auth)