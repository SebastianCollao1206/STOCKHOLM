from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    
    try:
        with app.app_context():
            db.engine.connect()
            print("Conexión exitosa a la base de datos LenguajesDB")
    except Exception as e:
        print(f"Error de conexión a la base de datos: {e}")
        
    return db