from fastapi import FastAPI
from mangum import Mangum
from app.routers import users, auth

app = FastAPI()

# Incluir routers
app.include_router(users.router, prefix="/user", tags=["user"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

# Mangum permite que FastAPI funcione con AWS Lambda
handler = Mangum(app)
