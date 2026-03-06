# Nina Confectionery Backend – FastAPI DDD Project

Backend for Nina Confectionery, built with FastAPI. Manages clients, orders, records, tasks, and payments, featuring CRUD operations, authentication, and Redis caching. Designed with Clean Architecture and Domain-Driven Design (DDD) principles.

---

## Architecture

The project follows Clean Architecture with layers:
  - Domain – Core business logic and entities
  - Application – Use cases and services
  - Infrastructure – Database, Redis, external services
  - Presentation – API routes and controllers

---

## Project Structure

```
app/
├── modules/      # Business modules (Bounded Contexts)
├── shared/       # Shared code and utilities
├── core/         # Central configuration
└── main.py       # Entry point
```

## Getting Started

1. Clone the repository
2. Copy `.env.example` to `.env` and configure your environment
3. Install dependencies: `poetry install`
4. Run the app: `uvicorn app.main:app --reload`

---

## Database Migrations

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

---

## Features:
  - CRUD operations for clients, orders, tasks, payments
  - Authentication and authorization
  - Redis caching for improved performance
  - Clean Architecture & DDD structure

---

## Technologies
Python • FastAPI • PostgreSQL • Redis • Alembic • Pytest • Docker
