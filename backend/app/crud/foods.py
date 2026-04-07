from sqlalchemy.orm import Session
from app.models.food import Food
from app.schemas.food import FoodCreate

def get_foods(db: Session, search: str = None, category: str = None, skip=0, limit=200):
    q = db.query(Food)
    if search:
        q = q.filter(Food.name_cs.ilike(f"%{search}%"))
    if category:
        q = q.filter(Food.category == category)
    return q.offset(skip).limit(limit).all()

def get_food(db: Session, food_id: int):
    return db.query(Food).filter(Food.id == food_id).first()

def create_food(db: Session, food: FoodCreate):
    db_food = Food(**food.model_dump())
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food

def calc_macros(food: Food, amount_g: float) -> dict:
    f = amount_g / 100.0
    return {
        "energy_kcal": round(food.energy_kcal * f, 1),
        "protein_g":   round(food.protein_g * f, 1),
        "carbs_g":     round(food.carbs_g * f, 1),
        "fat_g":       round(food.fat_g * f, 1),
        "fiber_g":     round(food.fiber_g * f, 1),
    }
