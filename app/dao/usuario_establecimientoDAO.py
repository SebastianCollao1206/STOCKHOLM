from app.config.connection import db
from sqlalchemy import text

class UsuarioEstablecimientoDAO:
    @staticmethod
    def crear_usuario_establecimiento(id_vendedor, id_establecimiento, id_usuario):
        try:
            query = text("CALL usp_nuevoUsuarioEstablecimiento(:p_idVendedor, :p_idEstablecimiento, :p_idUsuario)")
            db.session.execute(query, {
                'p_idVendedor': id_vendedor,
                'p_idEstablecimiento': id_establecimiento,
                'p_idUsuario': id_usuario
            })
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al crear relación usuario-establecimiento: {str(e)}")
    
    @staticmethod
    def actualizar_usuario_establecimiento(id_usuario_establecimiento, id_vendedor, id_establecimiento, id_usuario):
        try:
            query = text("CALL usp_actualizarUsuarioEstablecimiento(:p_idUsuarioEstablecimiento, :p_idVendedor, :p_idEstablecimiento, :p_idUsuario)")
            db.session.execute(query, {
                'p_idUsuarioEstablecimiento': id_usuario_establecimiento,
                'p_idVendedor': id_vendedor,
                'p_idEstablecimiento': id_establecimiento,
                'p_idUsuario': id_usuario
            })
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al actualizar relación usuario-establecimiento: {str(e)}")
    
    @staticmethod
    def obtener_info_por_id(id_usuario_establecimiento):
        try:
            query = text("CALL usp_obtenerInfoDeUsuarioEstablecimientoPorId(:p_idUsuarioEstablecimiento)")
            result = db.session.execute(query, {'p_idUsuarioEstablecimiento': id_usuario_establecimiento})
            row = result.fetchone()
            
            if row:
                return {
                    'idUsuarioEstablecimiento': row[0],
                    'idVendedor': row[1],
                    'idEstablecimiento': row[2],
                    'idUsuario': row[3]
                }
            return None
            
        except Exception as e:
            raise Exception(f"Error al obtener información de usuario-establecimiento: {str(e)}")
    
    @staticmethod
    def listar_usuario_establecimientos():
        try:
            query = text("CALL listarUsuarioEstablecimientos()")
            result = db.session.execute(query)
            return [dict(row) for row in result]  # Convertir a lista de diccionarios
            
        except Exception as e:
            raise Exception(f"Error al listar relaciones usuario-establecimiento: {str(e)}")
    
    @staticmethod
    def listar_usuario_establecimientos_por_usuario(id_usuario):
        try:
            query = text("CALL listarUsuarioEstablecimientosDeUsuario(:p_idUsuario)")
            result = db.session.execute(query, {'p_idUsuario': id_usuario})
            return [dict(row) for row in result]  # Convertir a lista de diccionarios
            
        except Exception as e:
            raise Exception(f"Error al listar establecimientos de usuario: {str(e)}")
