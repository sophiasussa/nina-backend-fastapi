# MyApp - FastAPI DDD Project

## 🏗️ Arquitetura

Projeto estruturado seguindo princípios de Clean Architecture e DDD.

## 📁 Estrutura

\`\`\`
app/
├── modules/      # Módulos de negócio (Bounded Contexts)
├── shared/       # Código compartilhado
├── core/         # Configurações centrais
└── main.py       # Entry point
\`\`\`

## 🚀 Como Executar

1. Clone o repositório
2. Copie `.env.example` para `.env` e configure
3. Instale dependências: `poetry install`
4. Execute: `uvicorn app.main:app --reload`

## 🧪 Testes

\`\`\`bash
pytest
pytest --cov=app tests/
\`\`\`

## 📝 Migrations

\`\`\`bash
alembic revision --autogenerate -m "description"
alembic upgrade head
\`\`\`
