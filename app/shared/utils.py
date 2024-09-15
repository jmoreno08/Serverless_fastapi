from fastapi import APIRouter, HTTPException
from app.shared.utils import log_action, validate_id, calculate_total

router = APIRouter()

# IDs permitidos para items
ALLOWED_ITEM_IDS = [1, 2, 3]

# Lista de precios de ejemplo
PRICES = [10.5, 20.0, 5.75]

@router.get("/items/")
def read_items():
    log_action("Fetching all items")
    return [{"item_id": 1, "name": "Item A"}, {"item_id": 2, "name": "Item B"}]

@router.get("/items/{item_id}")
def read_item(item_id: int):
    log_action(f"Fetching item with ID: {item_id}")

    # Validar si el ID del item está permitido
    if not validate_id(item_id, ALLOWED_ITEM_IDS):
        raise HTTPException(status_code=404, detail="Item not found")

    return {"item_id": item_id, "name": f"Item {item_id}"}

@router.get("/items/total")
def get_total_price():
    log_action("Calculating total price of items")
    total = calculate_total(PRICES)
    return {"total_price": total}