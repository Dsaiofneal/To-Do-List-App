from flask import Blueprint, jsonify, request
from models import task_repo

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.get('/tasks')
def list_tasks():
    return jsonify(task_repo.list_tasks())

@api_bp.post('/tasks')
def add_task():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'request body must be JSON'}), 400
    
    title = data.get('title')
    if not title:
        return jsonify({'error': 'title is required'}), 400
        
    task = task_repo.add_task(
        title=title.strip(),
        description=data.get('description'),
        priority=data.get('priority', 'medium'),
        category_id=data.get('category_id')
    )
    return jsonify(task), 201

@api_bp.get('/tasks/<int:task_id>')
def get_task(task_id):
    task = task_repo.get_task(task_id)
    return jsonify(task) if task else (jsonify({'error': 'Task not found'}), 404)

@api_bp.put('/tasks/<int:task_id>')
def update_task(task_id):
    data = request.get_json()
    task_repo.update_task(
        task_id, 
        data['title'], 
        data['description'], 
        data['status'], 
        data['priority']
    )
    return jsonify({'success': True})

@api_bp.delete('/tasks/<int:task_id>')
def delete_task(task_id):
    task_repo.delete_task(task_id)
    return jsonify({'success': True})
