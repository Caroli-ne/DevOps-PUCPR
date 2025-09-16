.PHONY: help build run stop test clean

# Variables
IMAGE_NAME = todo-api
CONTAINER_NAME = todo-api-container

help: ## Mostra esta mensagem de ajuda
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

build: ## Constrói a imagem Docker
	docker build -t $(IMAGE_NAME) .

run: ## Executa o container
	docker run -d --name $(CONTAINER_NAME) -p 8000:8000 $(IMAGE_NAME)

run-dev: ## Executa com docker-compose para desenvolvimento
	docker-compose up --build

stop: ## Para o container
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

logs: ## Mostra os logs do container
	docker logs -f $(CONTAINER_NAME)

test: ## Executa os testes dentro de um container
	docker run --rm $(IMAGE_NAME) pytest tests/ -v

test-local: ## Executa os testes localmente
	pytest tests/ -v

clean: ## Remove imagens e containers não utilizados
	docker system prune -f
	docker-compose down --volumes --remove-orphans

shell: ## Acessa o shell do container
	docker exec -it $(CONTAINER_NAME) /bin/bash

health: ## Verifica a saúde da aplicação
	@echo "Verificando saúde da aplicação..."
	@curl -f http://localhost:8000/health || echo "Aplicação não está respondendo"

docs: ## Abre a documentação da API no navegador
	@echo "Documentação disponível em:"
	@echo "- Swagger UI: http://localhost:8000/docs"
	@echo "- ReDoc: http://localhost:8000/redoc"
