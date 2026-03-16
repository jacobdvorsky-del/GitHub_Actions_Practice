from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes import bp
    from app.task_routes import task_bp
    app.register_blueprint(bp)
    app.register_blueprint(task_bp, url_prefix="/api")
    
    return app