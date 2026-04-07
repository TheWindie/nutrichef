# NutriChef — Claude SKILLS 🤖
> Tento soubor slouží jako kontext pro Claude při práci s projektem NutriChef.
> Přečti ho vždy na začátku každé session týkající se tohoto projektu.

---

## 1. O projektu

NutriChef je webová aplikace pro sledování a plánování jídelníčku pro dva uživatele:
- **Radim** (ID: 1) — cíl 75 kg, 2100 kcal/den, porce vždy `r` v datech
- **Monika** (ID: 2) — cíl 60 kg, 1450 kcal/den, porce vždy `m` v datech

## 2. Stack — co kde je

| Co | Kde | Jak spustit |
|----|-----|-------------|
| FastAPI backend | `backend/app/` | `uvicorn app.main:app --reload` |
| PostgreSQL | Docker kontejner `db` | port 5432 |
| Frontend | `frontend/` | servovaný přes nginx na portu 3000 |
| API docs | automatické | http://localhost:8000/docs |

## 3. Datový model — klíčové tabulky

### `foods` — potraviny (nutridatabaze.cz)
```
id, name_cs, name_en, category, subcategory,
energy_kcal, energy_kj,
protein_g, carbs_g, fat_g, fiber_g, sugar_g,
sat_fat_g, salt_g, water_g,
source, source_id,
created_at, updated_at
```
> Všechny hodnoty jsou na **100 g jedlého podílu** (standard nutridatabaze.cz).

### `meal_plans` — jídelní plány
```
id, name, user_id, week_start, notes, created_at
```

### `days` — den v plánu
```
id, plan_id, day_of_week (0=Po..6=Ne), notes
```

### `meals` — jídlo v rámci dne
```
id, day_id, meal_type (breakfast/lunch/dinner/snack),
name, instructions, sort_order
```

### `meal_ingredients` — suroviny jídla
```
id, meal_id, food_id,
amount_radim_g, amount_monika_g,
note
```

## 4. API endpointy

| Metoda | URL | Popis |
|--------|-----|-------|
| GET | /api/foods | Všechny potraviny (+ ?search=) |
| GET | /api/foods/{id} | Detail potraviny |
| POST | /api/foods | Přidat potravinu |
| GET | /api/plans | Jídelní plány |
| GET | /api/plans/{id} | Kompletní plán s makry |
| POST | /api/plans | Nový plán |
| GET | /api/plans/{id}/shopping | Nákupní seznam |
| GET | /api/plans/{id}/macros | Makra pro Radima + Moniku |

## 5. Výpočty — jak Claude počítá makra

```python
# Vzorec: hodnota = (food.nutrient_per_100g / 100) * amount_g
def calc(nutrient_per_100g: float, amount_g: float) -> float:
    return round(nutrient_per_100g / 100 * amount_g, 1)
```

Energie dle EU 1169/2011:
- Bílkoviny: 4 kcal/g
- Sacharidy: 4 kcal/g  
- Tuky: 9 kcal/g
- Vláknina: 2 kcal/g

## 6. Nutriční databáze — zdroj dat

Data pocházejí z **nutridatabaze.cz** (ÚZEI / Ministerstvo zemědělství ČR).
- Standard: EuroFIR
- Hodnoty: na 100 g jedlého podílu, syrový stav
- Kategorie: viz `data/seeds/foods_db.json`

Při přidávání nové potraviny VŽDY uveď:
- `source: "nutridatabaze.cz"` nebo `"manual"` nebo `"label"`
- `source_id`: kód z nutridatabaze (pokud dostupný)

## 7. Docker — jak deployovat

```bash
# Produkce
docker compose up -d

# Dev (hot reload)
docker compose -f docker-compose.dev.yml up

# Reset DB + reseed
docker compose exec backend alembic downgrade base
docker compose exec backend alembic upgrade head
docker compose exec backend python -m app.seeds.run
```

## 8. Konvence pro Claude

### Při úpravě jídelníčku:
1. Vždy zobraz náhled změny PŘED zápisem
2. Přepočítej makra pro oba uživatele
3. Upozorni pokud kcal překročí cíl o více než 10 %

### Při přidávání potraviny do DB:
1. Zkontroluj zda již neexistuje (`name_cs` ILIKE search)
2. Hodnoty zaokrouhli na 1 desetinné místo
3. Kategorie musí být z povoleného seznamu (viz foods_db.json)

### Při změně kódu:
1. Backend: vždy spusť `alembic revision --autogenerate` po změně modelu
2. Frontend: JS je vanilla, bez bundleru — přímé `<script type="module">`
3. Docker: po změně requirements.txt rebuild image

## 9. Frontend — struktura souborů

```
frontend/
├── index.html              Hlavní stránka — nav, sekce, boot() skript
├── src/
│   ├── api.js              Všechna volání na /api/* (fetch wrappery)
│   ├── state.js            Globální stav (plan, shopping, foods)
│   ├── utils.js            fmt(), fmtG(), sumMacros(), pct(), MEAL_LABELS
│   ├── components.js       macroCard(), mealBlock(), ingredientRow()
│   └── views/
│       ├── dashboard.js    renderDashboard(el) — hero + chart.js
│       ├── menu.js         renderMenu(el) — 7 dní × jídla
│       └── shopping.js     renderShopping(el) — nákupní seznam
```

Frontend je čistý vanilla JS s ES modules (`type="module"`).
Žádný bundler, žádný build krok — přímé `<script type="module">` v index.html.
Stylování: Tailwind CSS CDN + vlastní CSS v `<style>`.

## 10. Povolené kategorie potravin

```
maso_drubez, maso_hovezi, maso_veprove, maso_ryby,
mlecne_vyrobky, vejce,
obili_pecivo, lustediny,
zelenina, ovoce,
tuky_oleje, orechy_seminka,
napoje, ostatni
```
