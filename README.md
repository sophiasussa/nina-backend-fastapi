# 🍰 Nina Confectionery — Authentication Module

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-latest-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/PostgreSQL-14%2B-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Redis-7%2B-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
  <img src="https://img.shields.io/badge/Docker-ready-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/DDD-Clean%20Architecture-8A2BE2?style=for-the-badge" alt="DDD and Clean Architecture">
</p>

> Authentication module developed as part of **Nina Confectionery**, a planned management platform for confectionery businesses. The module provides secure authentication and customer management using **FastAPI, PostgreSQL, Redis, JWT, Clean Architecture, and Domain-Driven Design (DDD)**.

---

## 📑 Table of Contents

* [About the Project](#-about-the-project)
* [Features](#-features)
* [Technology Stack](#-technology-stack)
* [Architecture](#-architecture)
* [Project Structure](#-project-structure)
* [Prerequisites](#-prerequisites)
* [Running with Docker](#-running-with-docker-recommended)
* [Running Locally](#-running-locally)
* [Database Migrations](#-database-migrations)
* [Environment Variables](#-environment-variables)
* [API Documentation](#-api-documentation)
* [Testing](#-testing)

---

## 🧁 About the Project

The **Nina Confectionery Authentication Module** is an authentication and customer management component developed for the future Nina Confectionery management platform.

The project follows a modular architecture focused on **separation of concerns, security, testability, and maintainability**.

The current implementation includes:

* Authentication
* User identity management
* Customer management

The following modules are **not currently implemented**:

* Orders
* Products
* Recipes
* Tasks
* Payments

---

## 🔐 Features

### Authentication

* 👤 **User Registration** — user creation and validation
* 🔑 **Authentication** — user login and credential validation
* 🎟️ **JWT Authentication** — access token generation and validation
* 🔄 **Token Management** — access tokens, rotating refresh tokens, logout, and token revocation
* 🔒 **Password Security** — secure password storage and validation
* 🔑 **Password Recovery** — password reset flow using temporary tokens
* 🔵 **Google Login** — authentication using Google ID tokens
* 🗄️ **User Persistence** — user data stored in PostgreSQL

### Customer Management

* 👤 **Customer Registration**
* 🔎 **Customer Search**
* 📄 **Pagination**
* 🔄 **Customer Updates**
* 🏠 **Address Updates**
* ✅ **Customer Activation**
* ⛔ **Customer Deactivation**
* 🗑️ **Customer Deletion**

### Infrastructure & Quality

* ⚡ **Redis Integration** — refresh sessions, revoked access tokens, and password-reset tokens
* 🧪 **Automated Testing** — unit and integration tests covering domain rules, application use cases, routes, and infrastructure components
* 🐳 **Docker Support** — development environment using Docker Compose
* 🗃️ **Database Migrations** — managed with Alembic

> 🚧 Orders, products, recipes, tasks, and payments are not currently part of the implemented scope.

---

## 🛠 Technology Stack

| Layer                 | Technology               |
| --------------------- | ------------------------ |
| Language              | Python 3.11+             |
| Web Framework         | FastAPI                  |
| ORM                   | SQLAlchemy 2.x           |
| Migrations            | Alembic                  |
| Database              | PostgreSQL 14+           |
| Cache / Storage       | Redis 7+                 |
| Authentication        | JWT                      |
| Validation            | Pydantic v2              |
| ASGI Server           | Uvicorn                  |
| Containerization      | Docker + Docker Compose  |
| Testing               | Pytest                   |
| Architecture          | Clean Architecture + DDD |
| Dependency Management | pip                      |

---

## 🏛 Architecture

The project follows **Clean Architecture** principles combined with **Domain-Driven Design (DDD)**.

The architecture keeps business rules independent from frameworks and infrastructure details, allowing the system to remain easier to test, maintain, and evolve.

```text
┌─────────────────────────────────────────┐
│           Presentation Layer            │
│        FastAPI Routes / Schemas         │
├─────────────────────────────────────────┤
│            Application Layer            │
│           Use Cases / Services          │
├─────────────────────────────────────────┤
│              Domain Layer               │
│      Entities / Value Objects / Rules   │
├─────────────────────────────────────────┤
│          Infrastructure Layer           │
│        PostgreSQL / Redis / JWT         │
└─────────────────────────────────────────┘
```

### Domain

Contains entities, value objects, domain rules, and domain exceptions without direct dependencies on external infrastructure.

### Application

Contains use cases responsible for orchestrating business workflows and coordinating interactions between the domain and infrastructure layers.

### Infrastructure

Contains concrete implementations for persistence, database access, Redis, authentication mechanisms, and other external dependencies.

### Presentation

Contains HTTP routes, request/response schemas, and API-related components implemented with FastAPI.

Authentication and customer management are organized into independent modules, each following the same layered architecture.

---

## 📁 Project Structure

```text
nina-confectionery-backend/
├── app/
│   ├── main.py
│   ├── core/
│   ├── infra/
│   ├── shared/
│   └── modules/
│       ├── auth/
│       │   ├── domain/
│       │   ├── application/
│       │   ├── infrastructure/
│       │   └── presentation/
│       └── customer/
│           ├── domain/
│           ├── application/
│           ├── infrastructure/
│           └── presentation/
├── alembic/
├── docs/
│   └── postman/
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
├── alembic.ini
└── .env.example
```

---

## ✅ Prerequisites

For running with Docker:

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/)

For running locally:

* [Python 3.11+](https://www.python.org/downloads/)
* pip
* [Git](https://git-scm.com/)

---

## 🐳 Running with Docker (Recommended)

The easiest way to run the development environment is with Docker Compose.

The environment includes:

* FastAPI
* PostgreSQL
* Redis

### 1. Clone the repository

```bash
git clone https://github.com/sua-org/nina-confectionery-backend.git
cd nina-confectionery-backend
```

### 2. Configure environment variables

```bash
cp .env.example .env
```

Edit the `.env` file and configure the required values.

### 3. Start the containers

```bash
docker-compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

### Useful commands

Run in detached mode:

```bash
docker-compose up -d --build
```

Follow API logs:

```bash
docker-compose logs -f api
```

Stop all services:

```bash
docker-compose down
```

Stop services and remove volumes:

```bash
# ⚠️ This removes database and Redis data
docker-compose down -v
```

Access the API container:

```bash
docker-compose exec api bash
```

> ⚠️ Database migrations are not executed automatically. After starting the containers, run:

```bash
docker-compose exec api alembic upgrade head
```

---

## 💻 Running Locally

If you prefer to run the project without Docker:

### 1. Clone the repository

```bash
git clone https://github.com/sua-org/nina-confectionery-backend.git
cd nina-confectionery-backend
```

### 2. Create and activate a virtual environment

#### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

#### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements-dev.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Configure the required variables:

```text
DATABASE_URL
REDIS_HOST
REDIS_PORT
REDIS_DB
SECRET_KEY
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the server

```bash
uvicorn app.main:app --reload
```

---

## 🗃 Database Migrations

Database migrations are managed using **Alembic**.

### Apply pending migrations

Local:

```bash
alembic upgrade head
```

Docker:

```bash
docker-compose exec api alembic upgrade head
```

### Create a new migration

After creating or modifying a SQLAlchemy model:

```bash
alembic revision --autogenerate -m "description_of_change"
```

### Other useful commands

Show the current migration:

```bash
alembic current
```

Show migration history:

```bash
alembic history --verbose
```

Roll back the latest migration:

```bash
alembic downgrade -1
```

Roll back to a specific revision:

```bash
alembic downgrade <revision_id>
```

---

## 🔐 Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Application
APP_ENV=development
DEBUG=true
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/nina_db

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# CORS
ALLOWED_ORIGINS=["http://localhost:3000","http://localhost:8081"]
```

> ⚠️ Never commit your `.env` file. It should remain listed in `.gitignore`.

---

## 📡 API Documentation

### Swagger / ReDoc

With the application running, access:

* **Swagger UI:** http://localhost:8000/docs
* **ReDoc:** http://localhost:8000/redoc

### Postman

The Postman collection is available in:

```text
docs/postman/
```

Import the `.json` collection directly into Postman to access the configured endpoints.

All application routes are mounted under:

```text
/api/v1
```

### Authentication Routes

The authentication module currently provides:

* Registration
* Login
* Current-user lookup
* Token refresh
* Logout
* Logout from all sessions
* Forgot password
* Reset password
* Google login

### Customer Routes

The customer module currently provides:

* Create
* List/search
* Pagination
* Status filtering
* Get customer
* Update
* Address update
* Activate
* Deactivate
* Delete

> **Password recovery:** the reset link is currently generated and logged to the API process output. No email is sent yet.

> **Google login:** Google ID tokens are validated against the configured `GOOGLE_CLIENT_ID`. A valid client ID must be configured before using this functionality.

### Endpoints

| Endpoint            | Description                        |
| ------------------- | ---------------------------------- |
| `/api/v1/auth`      | Authentication and user management |
| `/api/v1/customers` | Authenticated customer management  |

---

## 🧪 Testing

The project uses **Pytest** for automated testing across the domain, application, presentation, and infrastructure layers.

The test suite currently covers areas including:

* Domain entities and value objects
* Authentication use cases
* Customer use cases
* API routes
* Google token verification
* Health endpoint
* Integration scenarios

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run the complete test suite:

```bash
pytest
```

For verbose output:

```bash
pytest -v
```

---

<p align="center">
  Built with 🍰 for Nina Confectionery.
</p>
