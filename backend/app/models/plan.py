from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum as SAEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.food import MealType

class User(Base):
    __tablename__ = "users"
    id         = Column(Integer, primary_key=True)
    name       = Column(String(50), nullable=False)
    target_kcal = Column(Integer, default=2000)
    target_kg  = Column(Float)
    color      = Column(String(10), default="emerald")
    plans      = relationship("MealPlan", back_populates="user")

class MealPlan(Base):
    __tablename__ = "meal_plans"
    id         = Column(Integer, primary_key=True)
    name       = Column(String(200), nullable=False)
    user_id    = Column(Integer, ForeignKey("users.id"))
    week_start = Column(DateTime(timezone=True))
    notes      = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user       = relationship("User", back_populates="plans")
    days       = relationship("PlanDay", back_populates="plan", order_by="PlanDay.day_of_week")

class PlanDay(Base):
    __tablename__ = "plan_days"
    id           = Column(Integer, primary_key=True)
    plan_id      = Column(Integer, ForeignKey("meal_plans.id"))
    day_of_week  = Column(Integer, nullable=False)   # 0=Po, 6=Ne
    notes        = Column(Text)
    plan         = relationship("MealPlan", back_populates="days")
    meals        = relationship("Meal", back_populates="day", order_by="Meal.sort_order")

class Meal(Base):
    __tablename__ = "meals"
    id           = Column(Integer, primary_key=True)
    day_id       = Column(Integer, ForeignKey("plan_days.id"))
    meal_type    = Column(SAEnum(MealType), default=MealType.lunch)
    name         = Column(String(300), nullable=False)
    instructions = Column(Text)
    sort_order   = Column(Integer, default=0)
    day          = relationship("PlanDay", back_populates="meals")
    ingredients  = relationship("MealIngredient", back_populates="meal", cascade="all, delete-orphan")

class MealIngredient(Base):
    __tablename__ = "meal_ingredients"
    id              = Column(Integer, primary_key=True)
    meal_id         = Column(Integer, ForeignKey("meals.id"))
    food_id         = Column(Integer, ForeignKey("foods.id"))
    amount_radim_g  = Column(Float, default=0.0)
    amount_monika_g = Column(Float, default=0.0)
    note            = Column(String(200))
    meal            = relationship("Meal", back_populates="ingredients")
    food            = relationship("Food", back_populates="ingredients")
