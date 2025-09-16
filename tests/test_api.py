from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Todo API - Sistema de Gerenciamento de Tarefas"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_create_task():
    task_data = {
        "title": "Teste de tarefa",
        "description": "Descrição do teste"
    }
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["completed"] == False
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_get_tasks():
    # Primeiro cria uma tarefa
    task_data = {"title": "Tarefa para listar", "description": "Teste"}
    client.post("/tasks", json=task_data)
    
    # Depois lista todas
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_task_by_id():
    # Cria uma tarefa
    task_data = {"title": "Tarefa específica", "description": "Teste específico"}
    create_response = client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    # Busca por ID
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == task_data["title"]

def test_get_nonexistent_task():
    response = client.get("/tasks/nonexistent-id")
    assert response.status_code == 404

def test_update_task():
    # Cria uma tarefa
    task_data = {"title": "Tarefa para atualizar", "description": "Original"}
    create_response = client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    # Atualiza a tarefa
    update_data = {"title": "Tarefa atualizada", "completed": True}
    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["completed"] == True

def test_delete_task():
    # Cria uma tarefa
    task_data = {"title": "Tarefa para deletar", "description": "Será deletada"}
    create_response = client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    # Deleta a tarefa
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    
    # Verifica se foi deletada
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404

def test_get_tasks_by_status():
    # Cria tarefas com diferentes status
    completed_task = {"title": "Tarefa completa", "description": "Completa"}
    incomplete_task = {"title": "Tarefa incompleta", "description": "Incompleta"}
    
    # Cria tarefa incompleta
    client.post("/tasks", json=incomplete_task)
    
    # Cria e completa uma tarefa
    create_response = client.post("/tasks", json=completed_task)
    task_id = create_response.json()["id"]
    client.put(f"/tasks/{task_id}", json={"completed": True})
    
    # Testa busca por completas
    response = client.get("/tasks/status/true")
    assert response.status_code == 200
    completed_tasks = response.json()
    assert any(task["completed"] == True for task in completed_tasks)
    
    # Testa busca por incompletas
    response = client.get("/tasks/status/false")
    assert response.status_code == 200
    incomplete_tasks = response.json()
    assert any(task["completed"] == False for task in incomplete_tasks)
