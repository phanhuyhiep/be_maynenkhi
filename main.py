import os
from fastapi import FastAPI
from routes.routerOrder import router_order
from routes.routerCategory import router_category
from routes.routerProduct import router_product
from routes.routerAuth import router_auth
from routes.routerCart import router_cart
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

port = os.environ.get('PORT')

app.include_router(router_category)
app.include_router(router_product)
app.include_router(router_auth)
app.include_router(router_cart)
app.include_router(router_order)

allow_origins=["*"]

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Server is online. Hello world!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)