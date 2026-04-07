"""
Seed skript — spusť jednou po `alembic upgrade head`:
    docker compose exec backend python -m app.seeds.run
"""
import json, os, sys
from pathlib import Path
from app.database import SessionLocal
from app.models.food import Food
from app.models.plan import User, MealPlan, PlanDay, Meal, MealIngredient

FOODS_FILE = Path("/data/seeds/foods_db.json")

def seed_foods(db):
    if db.query(Food).count() > 0:
        print("  ⏭  Potraviny již existují, přeskakuji.")
        return
    raw = FOODS_FILE.read_text(encoding="utf-8")
    data = json.loads(raw)
    foods = []
    for f in data["foods"]:
        foods.append(Food(
            source_id   = f.get("source_id"),
            name_cs     = f["name_cs"],
            name_en     = f.get("name_en"),
            category    = f.get("category"),
            energy_kcal = f["energy_kcal"],
            energy_kj   = f.get("energy_kj"),
            protein_g   = f.get("protein_g", 0),
            carbs_g     = f.get("carbs_g", 0),
            fat_g       = f.get("fat_g", 0),
            fiber_g     = f.get("fiber_g", 0),
            sugar_g     = f.get("sugar_g", 0),
            sat_fat_g   = f.get("sat_fat_g", 0),
            salt_g      = f.get("salt_g", 0),
            water_g     = f.get("water_g", 0),
            source      = "nutridatabaze.cz",
        ))
    db.bulk_save_objects(foods)
    db.commit()
    print(f"  ✅ Vloženo {len(foods)} potravin.")

def seed_users(db):
    if db.query(User).count() > 0:
        print("  ⏭  Uživatelé již existují, přeskakuji.")
        return
    db.add_all([
        User(id=1, name="Radim",  target_kcal=2100, target_kg=75.0, color="emerald"),
        User(id=2, name="Monika", target_kcal=1450, target_kg=60.0, color="rose"),
    ])
    db.commit()
    print("  ✅ Uživatelé Radim a Monika vytvořeni.")

def seed_plan(db):
    if db.query(MealPlan).count() > 0:
        print("  ⏭  Plán již existuje, přeskakuji.")
        return

    # Získáme ID potravin podle source_id
    def fid(source_id: str) -> int:
        food = db.query(Food).filter(Food.source_id == source_id).first()
        if not food:
            raise ValueError(f"Potravina {source_id} nenalezena — spusť nejdřív seed_foods")
        return food.id

    plan = MealPlan(id=1, name="Týdenní plán V1 — redukční", user_id=1)
    db.add(plan)
    db.flush()

    # Definice 7 dní (0=Po ... 6=Ne)
    DAYS = [
        # (day_of_week, [(meal_type, name, instructions, [(source_id, r_g, m_g)])])
        (0, [  # Pondělí
            ("breakfast", "Vejce na másle s šunkou a chlebem",
             "1. Na pánvi rozehřejte máslo. 2. Orestujte šunku a vejce na mírném ohni. 3. Podávejte s Breadway chlebem.",
             [("NDZ-0501",220,110),("NDZ-0203",90,60),("NDZ-0705",120,70),("NDZ-0612",8,5),("NDZ-0952",100,60)]),
            ("lunch", "Kuřecí prsa s mrkvovo-jogurtovým krémem",
             "1. Rýži uvařte v rýžovaru. 2. Kuře ogrilujte na kontaktním grilu. 3. Mrkev rozmixujte s jogurtem.",
             [("NDZ-0341",320,200),("NDZ-0701",110,70),("NDZ-1101",10,6),("NDZ-0603",60,40),("NDZ-0951",200,120)]),
            ("dinner", "Hovězí na cibuli se šťávou a bramborem",
             "1. Hovězí nakrájejte a duste s cibulí a bujónem. 2. Podávejte s vařeným bramborem.",
             [("NDZ-0101",270,160),("NDZ-0901",400,250),("NDZ-1101",10,6),("NDZ-0954",100,60),("NDZ-0104",100,60)]),
        ]),
        (1, [  # Úterý
            ("breakfast", "Tvarohové lívance s jogurtovým přelivem",
             "1. Rozmixujte tvaroh, vejce a mouku. 2. Smažte na lehce olejem potřené pánvi.",
             [("NDZ-0605",250,160),("NDZ-0709",75,45),("NDZ-0501",65,45),("NDZ-1101",5,3),("NDZ-0603",100,60)]),
            ("lunch", "Vepřová panenka s dijonským dipem a bramborovou kaší",
             "1. Panenku ogrilujte. 2. Brambory vyšlehejte s mlékem. 3. Dip: jogurt + dijonská hořčice.",
             [("NDZ-0201",310,190),("NDZ-0901",480,300),("NDZ-1302",20,15),("NDZ-1101",10,6),("NDZ-0602",60,40)]),
            ("dinner", "Krůtí tortilly se zakysanou smetanou",
             "1. Krůtí orestujte na oleji. 2. Tortilly nahřejte, potřete smetanou.",
             [("NDZ-0350",250,150),("NDZ-0707",180,100),("NDZ-0608",90,60),("NDZ-1101",10,6),("NDZ-0952",150,100)]),
        ]),
        (2, [  # Středa
            ("breakfast", "Cottage bowl s hořčicí a žitným toastem",
             "1. Cottage smíchejte s hořčicí a pažitkou. 2. Toast opečte nasucho.",
             [("NDZ-0610",250,160),("NDZ-0706",100,60),("NDZ-1301",20,15),("NDZ-0952",120,80)]),
            ("lunch", "Hovězí v rajčatové omáčce s rýží",
             "1. Hovězí duste s pasírovanými rajčaty, cibulí a bujónem. 2. Rýži uvařte v rýžovaru.",
             [("NDZ-0101",310,190),("NDZ-0956",250,150),("NDZ-0701",110,70),("NDZ-1101",10,6),("NDZ-0954",100,60)]),
            ("dinner", "Kuřecí s jogurtovým dresingem a bramborem",
             "1. Kuře orestujte na pánvi. 2. Jogurt smíchejte s česnekem a hořčicí.",
             [("NDZ-0341",310,190),("NDZ-0901",400,250),("NDZ-1302",15,10),("NDZ-0603",100,60),("NDZ-1101",10,6)]),
        ]),
    ]
        (3, [  # Čtvrtek
            ("breakfast", "Omeleta se sýrem a šunkou",
             "1. Vejce rozšlehejte s troškou vody. 2. Na másle orestujte šunku a sýr, zalijte vejci.",
             [("NDZ-0501",110,65),("NDZ-0609",60,40),("NDZ-0203",60,40),("NDZ-0612",8,5),("NDZ-0706",80,50)]),
            ("lunch", "Krůtí medailonky se špenátovo-tvarohovým krémem",
             "1. Krůtí ogrilujte. 2. Špenát poduste s česnekem, vmíchejte tvaroh. Podávejte s rýží.",
             [("NDZ-0350",320,200),("NDZ-0605",100,60),("NDZ-0958",150,100),("NDZ-0701",110,70),("NDZ-1101",10,6)]),
            ("dinner", "Mleté hovězí s paprikou a bramborem",
             "1. Mleté orestujte s paprikou a cibulí. 2. Podávejte s uvařeným bramborem.",
             [("NDZ-0103",280,170),("NDZ-0952",150,100),("NDZ-0901",400,250),("NDZ-1101",10,6),("NDZ-0954",80,50)]),
        ]),
        (4, [  # Pátek
            ("breakfast", "Šlehaný tvaroh s vlašskými ořechy a toastem",
             "1. Tvaroh vyšlehejte s troškou mléka. 2. Přidejte borůvky a ořechy. Podávejte s žitným toastem.",
             [("NDZ-0605",310,190),("NDZ-1201",40,25),("NDZ-1003",100,60),("NDZ-0706",80,50)]),
            ("lunch", "Kuřecí stehna s přírodní šťávou a bramborovou kaší",
             "1. Stehna pečte v troubě s cibulí. 2. Kaši připravte z brambor s mlékem.",
             [("NDZ-0342",450,280),("NDZ-0901",450,280),("NDZ-1101",10,6),("NDZ-0602",60,40),("NDZ-0954",100,60)]),
            ("dinner", "Červená čočka s vejcem a jogurtovým dipem",
             "1. Čočku uvařte v bujónu. 2. Vejce natvrdo. 3. Smíchejte s jogurtem a hořčicí.",
             [("NDZ-0801",110,70),("NDZ-0501",110,65),("NDZ-0603",100,60),("NDZ-0104",40,30),("NDZ-1302",15,10)]),
        ]),
        (5, [  # Sobota
            ("breakfast", "Vaječné muffiny se sýrem a šunkou",
             "1. Vejce rozšlehejte se špenátem a sýrem. 2. Pečte v fritéze ve formičkách.",
             [("NDZ-0501",135,85),("NDZ-0203",80,50),("NDZ-0609",40,25),("NDZ-0612",6,4),("NDZ-0706",80,50)]),
            ("lunch", "Hovězí steak s cibulovou redukcí a rýží",
             "1. Hovězí ogrilujte. 2. Cibuli zredukujte na pánvi s bujónem. 3. Rýže v rýžovaru.",
             [("NDZ-0101",330,200),("NDZ-0954",150,100),("NDZ-0701",110,70),("NDZ-1101",10,6),("NDZ-0104",50,30)]),
            ("dinner", "Kuřecí salát s mozzarellou a paprikou",
             "1. Kuře orestujte. 2. Smíchejte s mozzarellou, paprikou a jogurtovým přelivem.",
             [("NDZ-0341",280,170),("NDZ-0611",120,80),("NDZ-0952",180,120),("NDZ-0603",100,60),("NDZ-1101",10,6)]),
        ]),
        (6, [  # Neděle
            ("breakfast", "Žitný chléb s hummusem a vejcem",
             "1. Cizrnu rozmixujte s jogurtem a česnekem. 2. Namažte na chléb. Navrch ztracené vejce.",
             [("NDZ-0804",160,100),("NDZ-0501",110,65),("NDZ-0705",100,60),("NDZ-0952",100,60),("NDZ-0603",50,30)]),
            ("lunch", "Krůtí pečeně se zeleninovou omáčkou a kaší",
             "1. Krůtí pečte s mrkví. 2. Šťávu rozmixujte s mrkví. 3. Podávejte s bramborovou kaší.",
             [("NDZ-0350",350,210),("NDZ-0901",480,300),("NDZ-0951",200,120),("NDZ-1101",10,6),("NDZ-0104",60,40)]),
            ("dinner", "Šunkové závitky se sýrem a salátem",
             "1. Šunku potřete hořčicí, vložte sýr a srolujte. 2. Podávejte s toastem a zeleninou.",
             [("NDZ-0203",150,90),("NDZ-0609",80,50),("NDZ-0706",80,50),("NDZ-0963",200,120),("NDZ-1301",20,15)]),
        ]),
    ]

    for day_num, meals in DAYS:
        day = PlanDay(plan_id=1, day_of_week=day_num)
        db.add(day)
        db.flush()
        for sort, (mtype, name, instr, ings) in enumerate(meals):
            meal = Meal(day_id=day.id, meal_type=mtype, name=name,
                        instructions=instr, sort_order=sort)
            db.add(meal)
            db.flush()
            for (sid, r_g, m_g) in ings:
                db.add(MealIngredient(
                    meal_id=meal.id, food_id=fid(sid),
                    amount_radim_g=r_g, amount_monika_g=m_g
                ))
    db.commit()
    print("  ✅ Plán V1 (7 dní × 3 jídla) vložen.")

def run():
    db = SessionLocal()
    try:
        print("🌱 Seeding databáze...")
        seed_foods(db)
        seed_users(db)
        seed_plan(db)
        print("🎉 Seed dokončen.")
    except Exception as e:
        db.rollback()
        print(f"❌ Chyba: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    run()
