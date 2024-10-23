from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Database configuration - replace with your DATABASE_URL or local PostgreSQL connection string
database_url = os.environ.get('DATABASE_URL', 'postgresql://todo_user:welcome@localhost:5432/to_do_db')

# If the URL starts with 'postgres://', replace it with 'postgresql://'
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migration system
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Task model
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'task_name': self.task_name,
            'status': self.status
        }
@app.route('/')
def home():
    return "Welcome to the To-Do App! Go to /tasks to see the list of tasks.", 200

# Route to get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

# Route to add a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    new_task = request.json
    task_name = new_task.get('task_name')
    status = new_task.get('status', 'Pending')

    task = Task(task_name=task_name, status=status)
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task added successfully!"}), 201

# Route to get a task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return jsonify(task.to_dict())
    else:
        return jsonify({"message": "Task not found"}), 404

# Route to update a task by ID
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404

    update_data = request.json
    task.task_name = update_data.get('task_name', task.task_name)
    task.status = update_data.get('status', task.status)

    db.session.commit()
    return jsonify({"message": "Task updated successfully!"})

# Route to delete a task by ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully!"})

if __name__ == "__main__":
    app.run(debug=True)
