import pytest
from app import app, db, Task

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://todo_user:welcome@localhost:5432/to_do_db_test'
    
    with app.test_client() as client:
        with app.app_context():
            # Create the tables and setup initial state
            db.create_all()
            yield client
            db.drop_all()

def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200

def test_add_task(client):
    response = client.post('/tasks', json={"task_name": "Test Task", "status": "Pending"})
    assert response.status_code == 201
    assert b"Task added successfully!" in response.data

def test_get_task(client):
    client.post('/tasks', json={"task_name": "Test Task", "status": "Pending"})
    response = client.get('/tasks/1')
    assert response.status_code == 200

def test_update_task(client):
    client.post('/tasks', json={"task_name": "Test Task", "status": "Pending"})
    response = client.put('/tasks/1', json={"task_name": "Updated Task", "status": "Completed"})
    assert response.status_code == 200
    assert b"Task updated successfully!" in response.data

def test_delete_task(client):
    client.post('/tasks', json={"task_name": "Test Task", "status": "Pending"})
    response = client.delete('/tasks/1')
    assert response.status_code == 200
    assert b"Task deleted successfully!" in response.data
