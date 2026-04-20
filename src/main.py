from pathlib import Path
from flask import Flask, jsonify, send_file

from routes.task import task_bp

BASE_DIR = Path(__file__).resolve().parent

def create_app():
    app = Flask(__name__)
    app.register_blueprint(task_bp)
    
    @app.get('/')
    def home():
        return send_file(BASE_DIR / 'templates' / 'Index.html', mimetype='text/html; charset=utf-8')
    
    @app.get('/index.html') #catches the weird issue with the html link
    def link_home():
        return send_file(BASE_DIR / 'templates' / 'Index.html', mimetype='text/html; charset=utf-8')
    
    @app.get('/planner.html') 
    def planner():
        return send_file(BASE_DIR / 'templates' / 'planner.html', mimetype='text/html; charset=utf-8')
    
    return app
    
app = create_app()

if __name__ == '__main__':
    app.run(debug = True)