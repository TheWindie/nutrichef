from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import plans as crud

router = APIRouter()

@router.get("/")
def list_plans(db: Session = Depends(get_db)):
    plans = crud.get_plans(db)
    return [{"id": p.id, "name": p.name, "week_start": p.week_start} for p in plans]

@router.get("/{plan_id}")
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = crud.get_plan_full(db, plan_id)
    if not plan:
        raise HTTPException(404, "Plán nenalezen")
    return plan

@router.get("/{plan_id}/shopping")
def get_shopping(plan_id: int, db: Session = Depends(get_db)):
    result = crud.get_shopping_list(db, plan_id)
    if not result:
        raise HTTPException(404, "Plán nenalezen")
    return result

@router.get("/{plan_id}/macros")
def get_macros(plan_id: int, db: Session = Depends(get_db)):
    plan = crud.get_plan_full(db, plan_id)
    if not plan:
        raise HTTPException(404, "Plán nenalezen")
    return {
        "plan_id": plan_id,
        "days": [
            {
                "day_name": d["day_name"],
                "macros_radim": d["macros_radim"],
                "macros_monika": d["macros_monika"],
            }
            for d in plan["days"]
        ],
    }
