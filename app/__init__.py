from flask import Flask
from app.config.config import Config
from app.config.connection import init_db
from app.utils.notificaciones import Notificacion
from app.config.logging import setup_logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    setup_logging(app)
    
    init_db(app)
    
    @app.context_processor
    def inject_alert():
        from app.utils.notificaciones import Notificacion
        return dict(alert=Notificacion.get_alert())
    
    
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    
    return app