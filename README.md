* High-Concurrency Python REST API

[![Tests](https://github.com/YOUR-USERNAME/high-concurrency-python-rest-api/actions/workflows/tests.yml/badge.svg)](https://github.com/YOUR-USERNAME/high-concurrency-python-rest-api/actions/workflows/tests.yml)

A beginner-friendly asynchronous REST API built with **Python, FastAPI, SQLAlchemy, SQLite, Pydantic, pytest, and Locust**. It demonstrates CRUD endpoints, pagination, request metadata, basic metrics, automated tests, and a load-test scenario.

> Replace `YOUR-USERNAME` in the badge URL after creating your GitHub repository. This is a learning/demo project; do not claim specific throughput until you run and document a load test on your own hardware.

A step-by-step learning project using **Python, FastAPI, async SQLAlchemy, SQLite, Pydantic, pytest and Locust**.

## What you'll learn
- REST endpoints and HTTP methods
- Async/await and I/O concurrency
- CRUD operations with an async database session
- Input validation and response schemas
- Pagination, request IDs and basic metrics
- Automated tests and load testing

> This is a learning project, not a claim of a particular requests-per-second result. Measure performance on your own machine.

## 1. Install (Windows PowerShell)
Install Python 3.10+ first, then open a terminal in this folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

If activation is blocked, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal and activate again.

## 2. Run
```powershell
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs to interact with the API.

Other endpoints:
- `/health` — health check
- `/metrics` — in-process request count and average response time
- `/api/v1/tasks` — CRUD endpoints

## 3. Try it
In `/docs`, call `POST /api/v1/tasks` with:
```json
{"title":"Learn FastAPI","description":"Build my first async API","completed":false}
```
Then try `GET /api/v1/tasks`, `GET /api/v1/tasks/1`, `PATCH /api/v1/tasks/1`, and `DELETE /api/v1/tasks/1`. Use the actual ID returned by POST. Pagination example: `/api/v1/tasks?skip=0&limit=10`.

The local `tasks.db` database is created automatically.

## 4. Run tests
```powershell
pytest -v
```

## 5. Optional load test
```powershell
pip install locust
```
Start the API in terminal 1 with `uvicorn app.main:app`. In terminal 2:
```powershell
locust -f load_test/locustfile.py --host http://127.0.0.1:8000
```
Open http://localhost:8089, begin with a small number of users, then increase gradually. Only load-test systems you own or have permission to test. Record users, duration, requests/second, median and 95th percentile latency, failure percentage, and machine specs.

## Project structure
```text
app/
  main.py          # App setup and system endpoints
  database.py      # Async engine and session dependency
  models.py        # SQLAlchemy database model
  schemas.py       # Pydantic input/output schemas
  middleware.py    # Request ID, duration headers and basic metrics
  routes/tasks.py  # CRUD API
tests/test_tasks.py
load_test/locustfile.py
```

## How it works
1. A client sends an HTTP request.
2. FastAPI validates the request and routes it.
3. Middleware adds request metadata and tracks simple metrics.
4. The endpoint awaits database I/O through async SQLAlchemy.
5. FastAPI returns validated JSON.

## Interview explanation
**Why async?** It lets the event loop work on other I/O-bound requests while waiting for a database or network operation. It does not automatically speed up CPU-heavy work.

**Why pagination?** It limits response size and database work for each request.

**Why request IDs?** They help trace a request across logs.

**Limitations:** SQLite has write-concurrency limits; metrics are in memory and reset at restart; this demo has no authentication, rate limiting, or migrations.

**Production next steps:** PostgreSQL, Alembic migrations, authentication, rate limiting, structured logs, external metrics/tracing, caching where appropriate, and deployment tuning.

## GitHub description
Async FastAPI CRUD service with SQLite, Pydantic validation, pagination, request-ID middleware, health/metrics endpoints, automated tests, and a Locust load-test script.
