# Poster Maker — Backend

[![Python](https://img.shields.io/badge/Python-3.9-3776AB?logo=python&logoColor=white)](https://python.org/)
[![Django](https://img.shields.io/badge/Django-3.2-092E20?logo=django&logoColor=white)](https://djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.12-ff1709)](https://www.django-rest-framework.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)](https://docker.com/)
[![CI](https://github.com/AbhayParasharhere/Poster-Maker-Backend/actions/workflows/checks.yml/badge.svg)](https://github.com/AbhayParasharhere/Poster-Maker-Backend/actions/workflows/checks.yml)

> Django REST Framework API powering the Poster Maker platform for Punjab Insurance Canada — handles advisor authentication, user management, and poster data serving behind an nginx reverse proxy.

**Frontend Repo:** [Poster-maker-frontend →](https://github.com/AbhayParasharhere/Poster-maker-frontend)

---

## Architecture
```
React Frontend (Netlify)
        │
        │ HTTPS
        ▼
   nginx (reverse proxy)
        │
        ▼
Django REST API (uWSGI)
    ├── user/     → auth, registration, profile management
    └── core/     → poster data, models, business logic
        │
        ▼
   PostgreSQL
```

---

## Tech Stack

| Layer | Tech |
|-------|------|
| Framework | Django 3.2 + Django REST Framework 3.12 |
| API Docs | drf-spectacular (auto-generated OpenAPI schema) |
| Auth | DRF token auth + django-cors-headers |
| Database | PostgreSQL (psycopg2) |
| Image processing | Pillow |
| Server | uWSGI behind nginx |
| Containerization | Docker + Docker Compose |
| CI | GitHub Actions — test + flake8 lint on every push |

---

## Project Structure
```
app/
├── app/            # Django project settings, urls, wsgi/asgi
├── core/           # Models, admin, migrations, management commands
│   └── management/ # Custom management commands (e.g. wait_for_db)
├── user/           # Auth + user management app
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── manage.py
proxy/
├── Dockerfile      # nginx container
├── default.conf.tpl
└── uwsgi_params
scripts/
└── run.sh          # Entrypoint script
docker-compose.yml          # Local development
docker-compose-deploy.yml   # Production deployment
```

---

## Local Setup

**Prerequisites:** Docker + Docker Compose
```bash
# Clone
git clone https://github.com/AbhayParasharhere/Poster-Maker-Backend
cd Poster-Maker-Backend

# Configure environment
cp .env.sample .env
# Fill in DB credentials and Django secret key in .env

# Build and run
docker-compose build
docker-compose up
# → API available at http://localhost:8000
# → Auto-generated API docs at http://localhost:8000/api/docs/
```

---

## Running Tests & Lint
```bash
# Tests
docker-compose run --rm app sh -c "python manage.py wait_for_db && python manage.py test"

# Lint
docker-compose run --rm app sh -c "flake8"
```

These same commands run automatically on every push via GitHub Actions.

---

## Environment Variables

See `.env.sample` for all required variables. Key ones:

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `1` for local, `0` in prod |
| `DB_HOST` | PostgreSQL host |
| `DB_NAME` | Database name |
| `DB_USER` | Database user |
| `DB_PASS` | Database password |
| `ALLOWED_HOSTS` | Comma-separated allowed hostnames |

---

## CI/CD

GitHub Actions runs on every push:
1. Login to Docker Hub
2. Checkout code
3. Run test suite inside Docker (`wait_for_db` + `manage.py test`)
4. Run `flake8` lint check

---

## Contributors

Built as a paid client engagement for **Punjab Insurance Agency Inc.** (Canada).

| | GitHub |
|---|---|
| Abhay Parashar | [@AbhayParasharhere](https://github.com/AbhayParasharhere) |
| Naman Batra | [@nbatra752](https://github.com/nbatra752) |

---

## Related

| Repo | Description |
|------|-------------|
| [Poster-maker-frontend](https://github.com/AbhayParasharhere/Poster-maker-frontend) | React + Vite frontend |
| [PowerCompass Pro](https://powercompasspro.com) | Multi-tenant SaaS CRM — flagship project |
