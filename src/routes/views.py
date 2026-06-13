from flask import Blueprint, send_file
from config import BASE_DIR

views_bp = Blueprint('views', __name__)

@views_bp.get('/')
@views_bp.get('/index.html')
def home():
    return send_file(BASE_DIR / 'templates' / 'index.html', mimetype='text/html; charset=utf-8')

@views_bp.get('/planner.html')
def planner():
    return send_file(BASE_DIR / 'templates' / 'planner.html', mimetype='text/html; charset=utf-8')

@views_bp.get('/task.html')
def task_detail():
    return send_file(BASE_DIR / 'templates' / 'task.html', mimetype='text/html; charset=utf-8')
