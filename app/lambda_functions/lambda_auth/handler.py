from fastapi import FastAPI
from mangum import Mangum
from app.routers import auth

app = FastAPI()

app.include_router(auth.router,prefix="/auth",tags=["auth"])

handler = Mangum(app)
