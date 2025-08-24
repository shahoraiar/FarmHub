from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .auth import router as auth_router
from .user_routes import router as user_router
from .farm_routes import router as farm_router

app = FastAPI(title="FarmHub Reporting API")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(farm_router) 

@app.get("/")
def home():
    return {"msg": "FarmHub Reporting API"}
