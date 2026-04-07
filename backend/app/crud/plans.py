from sqlalchemy.orm import Session, joinedload
from app.models.plan import MealPlan, PlanDay, Meal, MealIngredient
from app.crud.foods import calc_macros
from app.schemas.plan import MacroSummary, DAY_NAMES

def get_plans(db: Session):
    return db.query(MealPlan).all()

def get_plan_full(db: Session, plan_id: int):
    plan = (db.query(MealPlan)
              .options(joinedload(MealPlan.days)
                       .joinedload(PlanDay.meals)
                       .joinedload(Meal.ingredients)
                       .joinedload(MealIngredient.food))
              .filter(MealPlan.id == plan_id)
              .first())
    if not plan:
        return None
    return _enrich_plan(plan)

def _zero() -> dict:
    return {"energy_kcal":0.0,"protein_g":0.0,"carbs_g":0.0,"fat_g":0.0,"fiber_g":0.0}

def _add(a: dict, b: dict) -> dict:
    return {k: round(a[k] + b[k], 1) for k in a}

def _enrich_plan(plan):
    result = {"id": plan.id, "name": plan.name,
              "week_start": plan.week_start, "notes": plan.notes, "days": []}
    for day in plan.days:
        day_r, day_m = _zero(), _zero()
        meals_out = []
        for meal in day.meals:
            meal_r, meal_m = _zero(), _zero()
            ings_out = []
            for ing in meal.ingredients:
                mr = calc_macros(ing.food, ing.amount_radim_g)
                mm = calc_macros(ing.food, ing.amount_monika_g)
                meal_r = _add(meal_r, mr)
                meal_m = _add(meal_m, mm)
                ings_out.append({"id": ing.id, "food_id": ing.food_id,
                    "food_name": ing.food.name_cs,
                    "amount_radim_g": ing.amount_radim_g,
                    "amount_monika_g": ing.amount_monika_g,
                    "macros_radim": mr, "macros_monika": mm,
                    "food_data": {
                        "energy_kcal": ing.food.energy_kcal,
                        "protein_g":   ing.food.protein_g,
                        "carbs_g":     ing.food.carbs_g,
                        "fat_g":       ing.food.fat_g,
                        "fiber_g":     ing.food.fiber_g,
                    }})
            day_r = _add(day_r, meal_r)
            day_m = _add(day_m, meal_m)
            meals_out.append({"id": meal.id, "meal_type": meal.meal_type,
                "name": meal.name, "instructions": meal.instructions,
                "ingredients": ings_out, "macros_radim": meal_r, "macros_monika": meal_m})
        result["days"].append({"id": day.id, "day_of_week": day.day_of_week,
            "day_name": DAY_NAMES[day.day_of_week],
            "meals": meals_out, "macros_radim": day_r, "macros_monika": day_m})
    return result

def get_shopping_list(db: Session, plan_id: int):
    plan = get_plan_full(db, plan_id)
    if not plan:
        return None
    agg = {}
    for day in plan["days"]:
        for meal in day["meals"]:
            for ing in meal["ingredients"]:
                key = (ing["food_id"], ing["food_name"])
                total = ing["amount_radim_g"] + ing["amount_monika_g"]
                agg[key] = agg.get(key, 0) + total
    items = []
    total_czk = 0
    for (fid, fname), qty in sorted(agg.items(), key=lambda x: x[0][1]):
        display = f"{qty/1000:.2f} kg" if qty >= 1000 else f"{round(qty)} g"
        est = round(qty * 0.23)
        total_czk += est
        items.append({"name": fname, "category": "", "total_g": qty,
                      "display": display, "estimated_czk": est})
    return {"plan_id": plan_id, "plan_name": plan["name"],
            "items": items, "estimated_czk": round(total_czk)}
