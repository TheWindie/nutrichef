from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import foods, plans, users

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="NutriChef API",
    description="Personalizovaný nutriční plánovač — Radim & Monika",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(foods.router,  prefix="/api/foods",  tags=["foods"])
app.include_router(plans.router,  prefix="/api/plans",  tags=["plans"])
app.include_router(users.router,  prefix="/api/users",  tags=["users"])

@app.get("/")
def root():
    return {"status": "ok", "app": "NutriChef", "docs": "/docs"}
