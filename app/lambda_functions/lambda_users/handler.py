from fastapi import FastAPI
from mangum import Mangum
from app.routers import users

app = FastAPI()

app.include_router(
    users.router,
    prefix="/user",
    tags=["user"]
)

handler = Mangum(app)

