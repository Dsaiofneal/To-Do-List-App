from flask import Blueprint, jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")

@tasks_bp.get("/")
def list_tasks():
    return jsonify([])