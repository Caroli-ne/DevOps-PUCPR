# Todo API - DevOps PUCPR

Uma API REST completa para gerenciamento de tarefas, desenvolvida como projeto prático para a disciplina de DevOps da PUCPR.

## 🚀 Funcionalidades

- ✅ Criar, listar, atualizar e deletar tarefas
- ✅ Marcar tarefas como completas/incompletas
- ✅ Filtrar tarefas por status
- ✅ Documentação automática com Swagger
- ✅ Testes automatizados
- ✅ Containerização com Docker

## 🛠️ Tecnologias

- **Python 3.11**
- **FastAPI** - Framework web moderno e rápido
- **Pydantic** - Validação de dados
- **Pytest** - Framework de testes
- **Docker** - Containerização
- **Uvicorn** - Servidor ASGI

## 📋 Estrutura do Projeto

```
├── src/
│   └── main.py          # Código principal da API
├── tests/
│   └── test_api.py      # Testes automatizados
├── docs/
├── requirements.txt     # Dependências Python
├── Dockerfile          # Configuração do container
└── README.md           # Documentação
```

## 🔧 Como Executar

### Localmente

1. **Clone o repositório:**
```bash
git clone https://github.com/Caroli-ne/DevOps-PUCPR.git
cd DevOps-PUCPR
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação:**
```bash
uvicorn src.main:app --reload
```

4. **Acesse a documentação:**
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Com Docker

1. **Build da imagem:**
```bash
docker build -t todo-api .
```

2. **Execute o container:**
```bash
docker run -p 8000:8000 todo-api
```

## 🧪 Executar Testes

```bash
pytest tests/ -v
```

## 📚 Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Mensagem de boas-vindas |
| GET | `/health` | Status da aplicação |
| POST | `/tasks` | Criar nova tarefa |
| GET | `/tasks` | Listar todas as tarefas |
| GET | `/tasks/{id}` | Buscar tarefa por ID |
| PUT | `/tasks/{id}` | Atualizar tarefa |
| DELETE | `/tasks/{id}` | Deletar tarefa |
| GET | `/tasks/status/{completed}` | Filtrar por status |

## 🎯 Objetivo do Projeto

Este projeto faz parte do aprendizado de **DevOps** e será usado para implementar um pipeline completo de **CI/CD**, incluindo:

- ✅ Controle de versão com Git
- ⏳ Testes automatizados
- ⏳ Build e deploy automatizados
- ⏳ Monitoramento e logs
- ⏳ Infraestrutura como código
