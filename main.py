from fastapi import FastAPI
from routes.routerOrder import router_order
from routes.routerCategory import router_category
from routes.routerProduct import router_product
from routes.routerAuth import router_auth
from routes.routerCart import router_cart
import uvicorn

app = FastAPI()

app.include_router(router_category)
app.include_router(router_product)
app.include_router(router_auth)
app.include_router(router_cart)
app.include_router(router_order)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

