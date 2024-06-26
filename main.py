from fastapi import FastAPI
from routes.routerCategory import router_category
from routes.routerProduct import router_product
from routes.routerAuth import router_auth
from routes.routerCart import router_cart

app = FastAPI()

app.include_router(router_category)
app.include_router(router_product)
app.include_router(router_auth)
app.include_router(router_cart)