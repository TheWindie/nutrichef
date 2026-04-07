from pydantic import BaseModel
from typing import Optional

class FoodBase(BaseModel):
    name_cs: str
    name_en: Optional[str] = None
    category: Optional[str] = None
    energy_kcal: float
    energy_kj: Optional[float] = None
    protein_g: float = 0.0
    carbs_g: float = 0.0
    fat_g: float = 0.0
    fiber_g: float = 0.0
    sugar_g: float = 0.0
    sat_fat_g: float = 0.0
    salt_g: float = 0.0
    water_g: float = 0.0
    source: str = "nutridatabaze.cz"
    source_id: Optional[str] = None

class FoodCreate(FoodBase):
    pass

class FoodRead(FoodBase):
    id: int
    class Config:
        from_attributes = True

class FoodNutrition(BaseModel):
    """Vypočtené makra pro zadané množství v gramech."""
    food_id: int
    food_name: str
    amount_g: float
    energy_kcal: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float

    @classmethod
    def from_food(cls, food, amount_g: float) -> "FoodNutrition":
        factor = amount_g / 100.0
        return cls(
            food_id=food.id,
            food_name=food.name_cs,
            amount_g=amount_g,
            energy_kcal=round(food.energy_kcal * factor, 1),
            protein_g=round(food.protein_g * factor, 1),
            carbs_g=round(food.carbs_g * factor, 1),
            fat_g=round(food.fat_g * factor, 1),
            fiber_g=round(food.fiber_g * factor, 1),
        )
