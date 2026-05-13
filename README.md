# 🍰 Nina Confectionery — Backend API

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-latest-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-14%2B-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Redis-7%2B-DC382D?style=for-the-badge&logo=redis&logoColor=white"/>
  <img src="https://img.shields.io/badge/Docker-ready-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
  <img src="https://img.shields.io/badge/DDD-Clean%20Architecture-8A2BE2?style=for-the-badge"/>
</p>

> Backend da **Nina Confectionery**, uma plataforma de gestão completa para confeitarias — gerenciando clientes, pedidos, fichas técnicas, tarefas e pagamentos, com autenticação, cache Redis e arquitetura robusta baseada em **Clean Architecture** e **DDD**.

---

## 📑 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Stack de Tecnologias](#-stack-de-tecnologias)
- [Arquitetura](#-arquitetura)
- [Estrutura de Pastas](#-estrutura-de-pastas)
- [Pré-requisitos](#-pré-requisitos)
- [Rodando com Docker](#-rodando-com-docker-recomendado)
- [Rodando Localmente](#-rodando-localmente)
- [Migrations com Alembic](#-migrations-com-alembic)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Documentação da API](#-documentação-da-api)
- [Testes](#-testes)

---

## 🧁 Sobre o Projeto

A **Nina Confectionery API** oferece toda a infraestrutura de backend para uma confeitaria moderna. A plataforma centraliza o gerenciamento do negócio em um único sistema:

- 👤 **Clientes** — cadastro, histórico e relacionamento
- 📦 **Pedidos** — criação, acompanhamento e status
- 📋 **Fichas Técnicas** — registros de receitas e produções
- ✅ **Tarefas** — organização interna e produção
- 💳 **Pagamentos** — controle financeiro e registros

---

## 🛠 Stack de Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.11+ |
| Framework Web | FastAPI |
| ORM | SQLAlchemy 2.x |
| Migrations | Alembic |
| Banco de Dados | PostgreSQL 14+ |
| Cache | Redis 7+ |
| Gerenciador de Deps | Poetry |
| Autenticação | JWT |
| Validação | Pydantic v2 |
| Servidor ASGI | Uvicorn |
| Containerização | Docker + Docker Compose |
| Testes | Pytest |

---

## 🏛 Arquitetura

O projeto segue os princípios de **Clean Architecture** combinados com **Domain-Driven Design (DDD)**, garantindo separação clara de responsabilidades e facilidade de manutenção e escala.

```
┌─────────────────────────────────────────┐
│           Presentation Layer            │  ← Rotas FastAPI, Controllers
├─────────────────────────────────────────┤
│           Application Layer             │  ← Use Cases, Services
├─────────────────────────────────────────┤
│             Domain Layer                │  ← Entidades, Regras de Negócio
├─────────────────────────────────────────┤
│          Infrastructure Layer           │  ← DB, Redis, Serviços Externos
└─────────────────────────────────────────┘
```

- **Domain** — Entidades, value objects e regras de negócio puras, sem dependências externas
- **Application** — Casos de uso que orquestram o domínio
- **Infrastructure** — Implementações concretas: banco, Redis, integrações
- **Presentation** — Rotas HTTP, schemas de entrada/saída, controllers

Cada módulo representa um **Bounded Context** do DDD, mantendo seu próprio domínio isolado.

---

## 📁 Estrutura de Pastas

```
nina-confectionery-backend/
├── app/
│   ├── main.py                  # Entrypoint da aplicação
│   ├── core/                    # Configurações centrais
│   │   ├── config.py            # Settings via Pydantic
│   ├── modules/                 # Bounded Contexts (DDD)
│   │   ├── auth/                
│   └── shared/                  # Código compartilhado
├── alembic/
│   ├── versions/                # Arquivos de migration
│   └── env.py
├── docs/
│   └── postman/                 # Coleção Postman da API
├── tests/
├── docker-compose.yml
├── Dockerfile
├── alembic.ini
├── pyproject.toml               # Configuração do Poetry
└── .env.example
```

---

## ✅ Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/install/) *(para rodar com Docker)*
- [Python 3.11+](https://www.python.org/downloads/) e [Poetry](https://python-poetry.org/docs/#installation) *(para rodar localmente)*
- [Git](https://git-scm.com/)

---

## 🐳 Rodando com Docker (recomendado)

A forma mais simples de subir toda a stack — **FastAPI + PostgreSQL + Redis** — com um único comando.

### 1. Clone o repositório

```bash
git clone https://github.com/sua-org/nina-confectionery-backend.git
cd nina-confectionery-backend
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
# Edite o .env com suas configurações, se necessário
```

### 3. Suba os containers

```bash
docker-compose up --build
```

A API estará disponível em `http://localhost:8000`.

### Comandos úteis

```bash
# Subir em segundo plano
docker-compose up -d --build

# Ver logs da API em tempo real
docker-compose logs -f api

# Parar todos os serviços
docker-compose down

# Parar e remover volumes (apaga o banco e o cache)
docker-compose down -v

# Acessar o shell do container da API
docker-compose exec api bash
```

> ⚠️ **As migrations não rodam automaticamente.** Após subir os containers, execute manualmente:
> ```bash
> docker-compose exec api alembic upgrade head
> ```

---

## 💻 Rodando Localmente

Caso prefira rodar sem Docker:

### 1. Clone e entre na pasta

```bash
git clone https://github.com/sua-org/nina-confectionery-backend.git
cd nina-confectionery-backend
```

### 2. Instale as dependências com Poetry

```bash
poetry install
poetry shell
```

### 3. Configure o ambiente

```bash
cp .env.example .env
# Configure DATABASE_URL, REDIS_URL e demais variáveis
```

### 4. Execute as migrations

```bash
alembic upgrade head
```

### 5. Inicie o servidor

```bash
uvicorn app.main:app --reload
```

---

## 🗃 Migrations com Alembic

> ⚠️ As migrations **não são executadas automaticamente** — precisam ser rodadas manualmente após subir o ambiente (local ou Docker).

### Aplicar todas as migrations pendentes

```bash
# Local
alembic upgrade head

# Docker
docker-compose exec api alembic upgrade head
```

### Criar uma nova migration

Após criar ou alterar um modelo SQLAlchemy:

```bash
alembic revision --autogenerate -m "descricao_da_alteracao"
```

### Outros comandos úteis

```bash
# Ver a migration atual aplicada no banco
alembic current

# Ver o histórico de migrations
alembic history --verbose

# Reverter a última migration
alembic downgrade -1

# Reverter até uma versão específica
alembic downgrade <revision_id>
```

---

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```env
# Aplicação
APP_ENV=development
DEBUG=true
SECRET_KEY=sua-chave-secreta-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Banco de Dados
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nina_db

# Redis
REDIS_URL=redis://localhost:6379/0

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8081
```

> ⚠️ Nunca commite o arquivo `.env`. Ele já está no `.gitignore`.

---

## 📡 Documentação da API

### Swagger / ReDoc (interativo)

Com a aplicação rodando, acesse:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Postman

A coleção Postman com todos os endpoints está disponível em:

```
docs/postman/
```

Importe o arquivo `.json` diretamente no Postman para ter acesso a todos os endpoints pré-configurados com exemplos de requisição.

### Endpoints principais

| Prefixo | Descrição |
|---|---|
| `/auth` | Login, registro, refresh de token |

---

<p align="center">
  Feito com 🍰 para a Nina Confectionery.
</p>
