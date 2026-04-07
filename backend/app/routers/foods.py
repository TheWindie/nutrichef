from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.crud import foods as crud
from app.schemas.food import FoodRead, FoodCreate

router = APIRouter()

@router.get("/", response_model=List[FoodRead])
def list_foods(
    search: Optional[str] = Query(None, description="Hledej v názvu (CZ)"),
    category: Optional[str] = Query(None),
    skip: int = 0, limit: int = 200,
    db: Session = Depends(get_db)
):
    return crud.get_foods(db, search=search, category=category, skip=skip, limit=limit)

@router.get("/categories")
def list_categories():
    return ["maso_drubez","maso_hovezi","maso_veprove","maso_ryby",
            "mlecne_vyrobky","vejce","obili_pecivo","lustediny",
            "zelenina","ovoce","tuky_oleje","orechy_seminka","ostatni"]

@router.get("/{food_id}", response_model=FoodRead)
def get_food(food_id: int, db: Session = Depends(get_db)):
    food = crud.get_food(db, food_id)
    if not food:
        raise HTTPException(404, "Potravina nenalezena")
    return food

@router.post("/", response_model=FoodRead, status_code=201)
def create_food(food: FoodCreate, db: Session = Depends(get_db)):
    return crud.create_food(db, food)
