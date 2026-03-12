from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel

security = HTTPBasic()
app = FastAPI()

user_db = [
    {"user_id": 1, "name": "Alice", "age": 30},
    {"user_id": 2, "name": "Bob", "age": 25},
    {"user_id": 3, "name": "Charlie", "age": 35},
]
item__db = [
    {"item_id": 10, "name": "Cake", "price": 10.0},
    {"item_id": 20, "name": "Coffee", "price": 5.0},
    {"item_id": 30, "name": "Hot Chocolate", "price": 3.0},
]


class User(BaseModel):
    user_id: int
    name: str
    age: int


class UserDeleteResponse(BaseModel):
    user_id: int
    deleted: bool = True


class Item(BaseModel):
    item_id: int
    name: str
    price: float


@app.get("/")
async def root():
    return {"message": "Hello World"}


def _get_user_from_db(user_id: int) -> dict | None:
    for user in user_db:
        if user["user_id"] == user_id:
            return user
    return None


def _get_item_from_db(item_id: int) -> dict | None:
    for item in item__db:
        if item["item_id"] == item_id:
            return item
    return None


def _check_credentials(credentials: HTTPBasicCredentials) -> bool:
    return credentials.username == "joulu" and credentials.password == "pukki"


@app.get("/user/{user_id}", response_model=User)
async def get_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)], user_id: int
):
    if not _check_credentials(credentials):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if user := _get_user_from_db(user_id):
        return User(**user)
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/user/{user_id}", response_model=UserDeleteResponse)
async def delete_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)], user_id: int
):
    if not _check_credentials(credentials):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if user := _get_user_from_db(user_id):
        return UserDeleteResponse(user_id=user["user_id"])
    raise HTTPException(status_code=404, detail="User not found")


@app.post("/user", response_model=User)
async def create_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)], user: User
):
    if not _check_credentials(credentials):
        raise HTTPException(status_code=401, detail="Unauthorized")
    if _get_user_from_db(user.user_id):
        raise HTTPException(status_code=400, detail="User already exists")
    return user


@app.get("/item/{item_id}", response_model=Item)
async def get_item(item_id: int):
    if item := _get_item_from_db(item_id):
        return Item(**item)
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/item/{item_id}", response_model=Item)
async def delete_item(item_id: int):
    if item := _get_item_from_db(item_id):
        return Item(**item)
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/item", response_model=Item)
async def create_item(item: Item):
    if _get_item_from_db(item.item_id):
        raise HTTPException(status_code=400, detail="Item already exists")
    return item
