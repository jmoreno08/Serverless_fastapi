from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.models import Item

router = APIRouter()

items = []

@router.get("/")
def list_items(user: str = Depends(get_current_user)):
    return items

@router.post("/")
def create_item(item: Item, user: str = Depends(get_current_user)):
    items.append(item)
    return item
