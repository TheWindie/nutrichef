from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.food import MealType

class MacroSummary(BaseModel):
    energy_kcal: float = 0.0
    protein_g: float = 0.0
    carbs_g: float = 0.0
    fat_g: float = 0.0
    fiber_g: float = 0.0

class IngredientRead(BaseModel):
    id: int
    food_id: int
    food_name: str
    amount_radim_g: float
    amount_monika_g: float
    macros_radim: MacroSummary
    macros_monika: MacroSummary
    class Config:
        from_attributes = True

class MealRead(BaseModel):
    id: int
    meal_type: MealType
    name: str
    instructions: Optional[str] = None
    ingredients: List[IngredientRead] = []
    macros_radim: MacroSummary
    macros_monika: MacroSummary
    class Config:
        from_attributes = True

DAY_NAMES = ["Pondělí","Úterý","Středa","Čtvrtek","Pátek","Sobota","Neděle"]

class PlanDayRead(BaseModel):
    id: int
    day_of_week: int
    day_name: str
    meals: List[MealRead] = []
    macros_radim: MacroSummary
    macros_monika: MacroSummary
    class Config:
        from_attributes = True

class PlanRead(BaseModel):
    id: int
    name: str
    week_start: Optional[datetime] = None
    notes: Optional[str] = None
    days: List[PlanDayRead] = []
    class Config:
        from_attributes = True

class ShoppingItem(BaseModel):
    name: str
    category: str
    total_g: float
    display: str  # "1.2 kg" nebo "350 g"

class ShoppingList(BaseModel):
    plan_id: int
    plan_name: str
    items: List[ShoppingItem]
    estimated_czk: float
