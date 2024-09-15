from fastapi import FastAPI, Depends
from mangum import Mangum
from app.routers import items
from app.auth import get_current_user

app = FastAPI()

app.include_router(
    items.router,
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_current_user)]
)

handler = Mangum(app)
