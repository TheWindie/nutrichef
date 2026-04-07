# 🍲 NutriChef

> Personalizovaný nutriční plánovač pro dva uživatele — 7denní jídelníček, makra, nákupní seznam.

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub_Actions-2088FF?logo=githubactions&logoColor=white)

---

## 📋 O projektu

NutriChef je webová aplikace pro plánování jídelníčku se zaměřením na redukční dietu.
Každé jídlo zobrazuje **odděleně porce a makra pro dva uživatele** s různými kalorickými cíli.

| Uživatel | Cíl | Kalorický příjem | Barva |
|----------|-----|-----------------|-------|
| **Radim** | 75 kg | ~2 100 kcal/den | 🟢 emerald |
| **Monika** | 60 kg | ~1 450 kcal/den | 🔴 rose |

---

## ✨ Funkce

- **Dashboard** — přehled cílů, predikce úbytku hmotnosti, průměrná makra (Chart.js)
- **7-denní menu** — každé jídlo s tabulkou ingrediencí, makry pro R+M a instrukcemi k přípravě
- **Nákupní seznam** — automatický součet surovin za celý týden s odhadem ceny (Rohlik.cz)
- **Databáze potravin** — ~55 potravin z nutridatabaze.cz (EuroFIR standard, ÚZEI), vyhledávání + filtr kategorií
- **REST API** — FastAPI s automatickými Swagger docs na `/docs`

---

## 🏗️ Architektura

```
┌─────────────────────────────────────────────────────┐
│                    Docker Stack                      │
│                                                     │
│  ┌──────────────┐    ┌──────────────────────────┐   │
│  │   nginx:alpine│    │   python:3.12-slim       │   │
│  │   Frontend   │───▶│   FastAPI Backend        │   │
│  │   port 3100  │    │   port 8000              │   │
│  └──────────────┘    └────────────┬─────────────┘   │
│                                   │                 │
│                      ┌────────────▼─────────────┐   │
│                      │   postgres:16-alpine      │   │
│                      │   PostgreSQL DB           │   │
│                      │   port 5432              │   │
│                      └──────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## 🗂️ Struktura projektu

```
nutrichef/
├── .claude/
│   └── SKILLS.md              # Instrukce pro Claude AI (kontext projektu)
├── .github/workflows/
│   └── docker-build.yml       # CI: build + push na ghcr.io
├── backend/
│   ├── app/
│   │   ├── main.py            # FastAPI entry point + CORS
│   │   ├── config.py          # pydantic-settings + .env
│   │   ├── database.py        # SQLAlchemy 2 engine + session
│   │   ├── models/            # ORM: Food, User, MealPlan, PlanDay, Meal, MealIngredient
│   │   ├── schemas/           # Pydantic schémata + FoodNutrition helper
│   │   ├── crud/              # calc_macros(), get_plan_full(), get_shopping_list()
│   │   ├── routers/           # GET/POST /foods, /plans, /users
│   │   └── seeds/run.py       # Import potravin + výchozí plán do DB
│   ├── alembic/               # Databázové migrace
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── index.html             # SPA: nav, 4 taby, ES module boot
│   ├── Dockerfile             # nginx:alpine + statické soubory
│   ├── nginx.conf             # Reverse proxy → backend:8000
│   └── src/
│       ├── api.js             # Fetch wrappery → /api/*
│       ├── state.js           # Reaktivní store (subscribe/notify)
│       ├── utils.js           # fmt, fmtG, sumMacros, pct, MEAL_LABELS
│       ├── components.js      # macroCard, mealBlock, ingredientRow
│       └── views/
│           ├── dashboard.js   # Hero + Chart.js graf
│           ├── menu.js        # 7 dní × jídla × ingredience
│           └── shopping.js    # Nákupní seznam + odhad ceny
├── data/seeds/
│   └── foods_db.json          # ~55 potravin (nutridatabaze.cz / EuroFIR)
├── docker-compose.yml         # Produkce (ghcr.io images)
├── docker-compose.dev.yml     # Dev (hot reload, local build)
├── deploy.sh                  # Deploy skript pro WindieLAB host
└── .env.example
```

## 🗄️ Datový model

```sql
foods              -- nutridatabaze.cz, ~55 položek, hodnoty /100g
users              -- Radim (2100 kcal), Monika (1450 kcal)
meal_plans         -- pojmenovaný plán (např. "Týdenní plán V1")
plan_days          -- den v týdnu (0=Po … 6=Ne)
meals              -- jídlo (breakfast/lunch/dinner/snack) + instrukce
meal_ingredients   -- surovina + amount_radim_g + amount_monika_g
```

## 🚀 Rychlý start — lokální vývoj

```bash
# 1. Klonování
git clone https://github.com/TheWindie/nutrichef.git
cd nutrichef

# 2. Prostředí
cp .env.example .env

# 3. Spuštění (dev — hot reload)
docker compose -f docker-compose.dev.yml up -d

# Frontend: http://localhost:3000
# API docs: http://localhost:8000/docs
```

## 🖥️ Deploy na WindieLAB (Dockhand)

Images se automaticky buildí přes GitHub Actions a pushují na `ghcr.io`.

### Možnost A — Dockhand "From Git"
1. Otevři Dockhand → Stacks → **From Git**
2. Zadej: `https://github.com/TheWindie/nutrichef`
3. Compose file: `docker-compose.yml`
4. Nastav environment variables (viz `.env.example`)

### Možnost B — Ručně na hostu
```bash
mkdir -p /opt/nutrichef/data/seeds
cd /opt/nutrichef

# Stáhni compose soubory
curl -O https://raw.githubusercontent.com/TheWindie/nutrichef/main/docker-compose.yml
curl -O https://raw.githubusercontent.com/TheWindie/nutrichef/main/.env.example
cp .env.example .env
nano .env  # nastav DB_PASSWORD, DATA_PATH

# Stáhni seed data
curl -o data/seeds/foods_db.json \
  https://raw.githubusercontent.com/TheWindie/nutrichef/main/data/seeds/foods_db.json

docker compose pull
docker compose up -d
```

App bude dostupná na: **`http://10.20.10.87:3100`**

### CI/CD pipeline

```
git push → GitHub Actions → docker build (amd64) → ghcr.io push
                                                         ↓
                                          docker compose pull (na hostu)
                                          docker compose up -d
```


## 📡 API přehled

| Metoda | Endpoint | Popis |
|--------|----------|-------|
| `GET` | `/api/foods/` | Seznam potravin (`?search=kuře&category=maso_drubez`) |
| `GET` | `/api/foods/{id}` | Detail potraviny |
| `POST` | `/api/foods/` | Přidat potravinu |
| `GET` | `/api/foods/categories` | Seznam kategorií |
| `GET` | `/api/plans/` | Seznam plánů |
| `GET` | `/api/plans/{id}` | Kompletní plán s makry |
| `GET` | `/api/plans/{id}/shopping` | Nákupní seznam |
| `GET` | `/api/plans/{id}/macros` | Makra po dnech |
| `GET` | `/api/users/` | Uživatelé |

Swagger UI: **`http://localhost:8000/docs`**

## 🥗 Nutriční databáze

Data pocházejí z **[nutridatabaze.cz](https://www.nutridatabaze.cz)** — oficiální česká databáze složení potravin spravovaná ÚZEI (Ministerstvo zemědělství ČR), standard EuroFIR.

- Hodnoty jsou na **100 g jedlého podílu**, syrový stav
- Energetická hodnota dle EU 1169/2011 (B=4 kcal/g, S=4 kcal/g, T=9 kcal/g, Vl=2 kcal/g)
- Kategorie: drůbež, hovězí, vepřové, ryby, mléčné, vejce, obiloviny, luštěniny, zelenina, ovoce, tuky, ořechy

## 🛠️ Stack

| Vrstva | Technologie | Verze |
|--------|-------------|-------|
| Backend | FastAPI + Uvicorn | 0.115 / 0.30 |
| ORM | SQLAlchemy 2 + Alembic | 2.0 / 1.13 |
| Databáze | PostgreSQL | 16 |
| Validace | Pydantic v2 | 2.9 |
| Frontend | Vanilla JS (ES modules) | — |
| Stylování | Tailwind CSS CDN | 3.x |
| Grafy | Chart.js CDN | latest |
| Web server | nginx:alpine | latest |
| Kontejnery | Docker + Docker Compose | — |
| CI/CD | GitHub Actions → ghcr.io | — |

## 📁 Klíčové soubory pro Claude

Při práci s projektem vždy přečti: **`.claude/SKILLS.md`**

Obsahuje: datový model, API endpointy, výpočetní vzorce, konvence, deploy postup.

---

*Projekt: NutriChef — WindieLAB / Windie s.r.o.*
