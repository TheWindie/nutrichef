from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class MealType(str, enum.Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"

class Food(Base):
    __tablename__ = "foods"
    id           = Column(Integer, primary_key=True, index=True)
    source_id    = Column(String(20), index=True)
    name_cs      = Column(String(200), nullable=False, index=True)
    name_en      = Column(String(200))
    category     = Column(String(50), index=True)
    energy_kcal  = Column(Float, nullable=False)
    energy_kj    = Column(Float)
    protein_g    = Column(Float, default=0.0)
    carbs_g      = Column(Float, default=0.0)
    fat_g        = Column(Float, default=0.0)
    fiber_g      = Column(Float, default=0.0)
    sugar_g      = Column(Float, default=0.0)
    sat_fat_g    = Column(Float, default=0.0)
    salt_g       = Column(Float, default=0.0)
    water_g      = Column(Float, default=0.0)
    source       = Column(String(50), default="nutridatabaze.cz")
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    ingredients  = relationship("MealIngredient", back_populates="food")
