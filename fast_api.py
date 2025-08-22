from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel

app = FastAPI()

# GET METHOD
# @app.get("/")
# async def root():
#     return {"messages": "Hello world"}

# @app.get("/users/{user_id}")
# async def get_user(user_id: int):
#     return {"user_id": user_id, "message": f"Hello user {user_id}"}

# @app.get("/items/")
# async def get_items(skip: int = 0, limit: int = 10):
#     return {"skip": skip, "limit": limit, "message": f"Items from {skip} to {skip+limit}"}


# POST METHOD
# class Item(BaseModel):
#     name: str
#     price: float
#     is_available: bool = True

# @app.post("/items/")
# async def create_item(item: Item):
#     return {"item": item, "messages": f"{item.name} created!"}


# PATH, QUERY
# @app.get("/products/{product_id}")
# async def get_product(
#     product_id: int = Path(..., ge=1), # Must be >= 1
#     category: str = Query(..., min_length=3) # Required, min length 3
# ):
#     return {"product_id": product_id, "category": category}


# HANDLING ERRORS
@app.get("/users/{user_id}")
async def get_user(user_id: int): 
    if user_id <= 1:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "message": f"Hey user {user_id}"}
