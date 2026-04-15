from flask import Flask, jsonify
from routes.tasks import tasks_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(tasks_bp)

    @app.get("/")
    def home():
        return "Tasking is running"

    @app.get("/api/health")
    def health():
        return jsonify({"ok": True})

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)