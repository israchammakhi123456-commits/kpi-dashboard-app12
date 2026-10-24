# KPI Dashboard (Flask + database, full CRUD)

- **Create / read / update / delete** KPIs (name, unit, target, higher/lower-is-better, color)
- **CRUD on measurements** (dated values) per KPI, CSV import / export
- Dashboard cards, history + 6-month forecast chart, progress chart, auto-generated alerts
- Optional password: set `ADMIN_PASSWORD` and only logged-in users can edit (everyone can view)

## Run locally
```
pip install -r requirements.txt
python app.py        # http://localhost:5000  (uses SQLite file kpi.db)
```

## Deploy on Render
1. Push this folder to a GitHub repo.
2. Render → New → **Blueprint** → pick the repo (it reads `render.yaml`, creates the web service + Postgres DB).
3. When asked, type a value for `ADMIN_PASSWORD`.

Env vars: `DATABASE_URL` (Postgres; falls back to SQLite), `ADMIN_PASSWORD`, `SECRET_KEY`, `SEED_SAMPLE=0` to start empty.
