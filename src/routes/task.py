from flask import Blueprint, jsonify, request

from routes.task_database import add_task as add_task_to_db
from routes.task_database import init_db, list_tasks as list_tasks_from_db

task_bp = Blueprint('Tasks', __name__, url_prefix='/task_file')

init_db()

@task_bp.get('/tasks')
def list_tasks():
    return jsonify(list_tasks_from_db())

@task_bp.post('/task_add')
def add_task():
    data = request.get_json(silent = True)
    if not data: #request body was missing or invalid JSON
        return jsonify({'error': 'request body must be JSON'}), 400
    
    title = data.get('title', data.get('field'))
    if not isinstance(title, str) or not title.strip():
        return jsonify({'error': 'title (or field) is required'}), 400
    
    task = add_task_to_db(title.strip())
    return jsonify(task), 201