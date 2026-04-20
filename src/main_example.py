from pathlib import Path

from flask import Flask, jsonify, send_file
from routes.tasks import tasks_bp

BASE_DIR = Path(__file__).resolve().parent

def create_app():
    app = Flask(__name__)
    app.register_blueprint(tasks_bp)

    @app.get("/")
    def home():
        return "Tasking is running"

    @app.get("/api/health")
    def health():
        return jsonify({"ok": True})

    @app.get("/learn/example/add-task")
    def add_task_example_file():
        return send_file(BASE_DIR / "docs" / "add_task_example.json", mimetype="application/json")

    @app.get("/learn/tutorial")
    def tutorial_file():
        return send_file(BASE_DIR / "docs" / "flask_tutorial.md", mimetype="text/markdown; charset=utf-8")
    
    @app.get('/tasks')
    def test():
        return send_file(BASE_DIR / 'docs' / 'tasks.py', mimetype='application/python')

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)