from app.config.connection import db
from sqlalchemy import text
from werkzeug.security import generate_password_hash

class UsuarioDAO:
    @staticmethod
    def crear_usuario(usuario, correo, clave):
        try:
            clave_hash = generate_password_hash(clave)
            
            query = text("CALL usp_nuevoUsuario(:p_usuario, :p_correo, :p_claveHash)")
            db.session.execute(query, {
                'p_usuario': usuario,
                'p_correo': correo,
                'p_claveHash': clave_hash
            })
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            if "Duplicate entry" in str(e):
                if "usuario" in str(e):
                    raise Exception("El nombre de usuario ya existe")
                elif "correo" in str(e):
                    raise Exception("El correo electrónico ya está registrado")
            raise Exception(f"Error al crear usuario: {str(e)}")
    
    @staticmethod
    def obtener_id_por_usuario(usuario):
        try:
            query = text("CALL usp_obtenerIdUsuarioPorUsuario(:p_usuario)")
            result = db.session.execute(query, {'p_usuario': usuario})
            row = result.fetchone()
            return row[0] if row else None
            
        except Exception as e:
            raise Exception(f"Error al obtener ID de usuario: {str(e)}")
    
    @staticmethod
    def obtener_info_usuario_por_id(id_usuario):
        try:
            query = text("CALL usp_obtenerInfoDeUsuarioPorId(:p_idUsuario)")
            result = db.session.execute(query, {'p_idUsuario': id_usuario})
            row = result.fetchone()
            
            if row:
                return {
                    'idUsuario': row[0],
                    'usuario': row[1],
                    'correo': row[2]
                }
            return None
            
        except Exception as e:
            raise Exception(f"Error al obtener información del usuario: {str(e)}")
    
    @staticmethod
    def obtener_hash_usuario_por_id(id_usuario):
        try:
            query = text("CALL usp_obtenerHashDeUsuarioPorId(:p_idUsuario)")
            result = db.session.execute(query, {'p_idUsuario': id_usuario})
            row = result.fetchone()
            return row[0] if row else None
            
        except Exception as e:
            raise Exception(f"Error al obtener hash del usuario: {str(e)}")
        
    @staticmethod
    def obtener_id_por_correo(correo):
        try:
            query = text("SELECT idUsuario FROM Usuario WHERE correo = :correo")
            result = db.session.execute(query, {'correo': correo})
            row = result.fetchone()
            return row[0] if row else None
            
        except Exception as e:
            raise Exception(f"Error al obtener ID por correo: {str(e)}")    
        
    @staticmethod
    def verificar_correo_existe(correo):
        try:
            query = text("SELECT COUNT(*) FROM Usuario WHERE correo = :correo")
            result = db.session.execute(query, {'correo': correo})
            count = result.fetchone()[0]
            return count > 0
            
        except Exception as e:
            raise Exception(f"Error al verificar correo: {str(e)}")    