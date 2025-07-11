from app.config.connection import db
from sqlalchemy import text

class EstablecimientoDAO:
    @staticmethod
    def crear_establecimiento(establecimiento, direccion, hora_apertura, hora_cierre, id_usuario):
        try:            
            query_est = text("CALL usp_nuevoEstablecimiento(:p_establecimiento, :p_direccion, :p_horaApertura, :p_horaCierre)")
            db.session.execute(query_est, {
                'p_establecimiento': establecimiento,
                'p_direccion': direccion,
                'p_horaApertura': hora_apertura,
                'p_horaCierre': hora_cierre
            })
            
            id_establecimiento = db.session.execute(text("SELECT LAST_INSERT_ID()")).fetchone()[0]
            
            query_rel = text("CALL usp_nuevoUsuarioEstablecimiento(:p_idVendedor, :p_idEstablecimiento, :p_idUsuario)")
            db.session.execute(query_rel, {
                'p_idVendedor': None,
                'p_idEstablecimiento': id_establecimiento,
                'p_idUsuario': id_usuario
            })
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al crear establecimiento: {str(e)}")
    
    @staticmethod
    def actualizar_establecimiento(id_establecimiento, establecimiento, direccion, hora_apertura, hora_cierre, id_usuario):
        try:
            if not EstablecimientoDAO._verificar_propiedad(id_establecimiento, id_usuario):
                raise Exception("No tienes permisos para editar este establecimiento")
            
            query = text("CALL usp_actualizarEstablecimiento(:p_idEstablecimiento, :p_establecimiento, :p_direccion, :p_horaApertura, :p_horaCierre)")
            db.session.execute(query, {
                'p_idEstablecimiento': id_establecimiento,
                'p_establecimiento': establecimiento,
                'p_direccion': direccion,
                'p_horaApertura': hora_apertura,
                'p_horaCierre': hora_cierre
            })
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al actualizar establecimiento: {str(e)}")
    
    # @staticmethod
    # def obtener_establecimiento_por_id(id_establecimiento, id_usuario):
    #     try:
    #         query = text("""
    #             SELECT e.idEstablecimiento, e.establecimiento, e.direccion, e.horaApertura, e.horaCierre
    #             FROM Establecimiento e
    #             INNER JOIN UsuarioEstablecimiento ue ON e.idEstablecimiento = ue.idEstablecimiento
    #             WHERE e.idEstablecimiento = :p_idEstablecimiento AND ue.idUsuario = :p_idUsuario
    #         """)
    #         result = db.session.execute(query, {
    #             'p_idEstablecimiento': id_establecimiento,
    #             'p_idUsuario': id_usuario
    #         })
    #         row = result.fetchone()
            
    #         if row:
    #             return {
    #                 'idEstablecimiento': row[0],
    #                 'establecimiento': row[1],
    #                 'direccion': row[2],
    #                 'horaApertura': EstablecimientoDAO._format_time_for_display(row[3]),
    #                 'horaCierre': EstablecimientoDAO._format_time_for_display(row[4])
    #             }
    #         return None
            
    #     except Exception as e:
    #         raise Exception(f"Error al obtener información del establecimiento: {str(e)}")
    
    @staticmethod
    def obtener_establecimiento_por_id(id_establecimiento, id_usuario):
        try:
            query = text("CALL usp_obtenerInfoDeEstablecimientoPorId(:p_idEstablecimiento)")
            result = db.session.execute(query, {
                'p_idEstablecimiento': id_establecimiento
            })
            row = result.fetchone()
            
            if row:
                return {
                    'idEstablecimiento': row[0],
                    'establecimiento': row[1],
                    'direccion': row[2],
                    'horaApertura': EstablecimientoDAO._format_time_for_display(row[3]),
                    'horaCierre': EstablecimientoDAO._format_time_for_display(row[4])
                }
            return None
            
        except Exception as e:
            raise Exception(f"Error al obtener información del establecimiento: {str(e)}")
    
    @staticmethod
    def contar_por_nombre(establecimiento, id_usuario, id_establecimiento_excluir=None):
        try:
            if id_establecimiento_excluir:
                query = text("""
                    SELECT COUNT(*) FROM Establecimiento e
                    INNER JOIN UsuarioEstablecimiento ue ON e.idEstablecimiento = ue.idEstablecimiento
                    WHERE e.establecimiento = :p_establecimiento 
                    AND ue.idUsuario = :p_idUsuario 
                    AND e.idEstablecimiento != :p_idEstablecimientoExcluir
                """)
                result = db.session.execute(query, {
                    'p_establecimiento': establecimiento,
                    'p_idUsuario': id_usuario,
                    'p_idEstablecimientoExcluir': id_establecimiento_excluir
                })
            else:
                query = text("""
                    SELECT COUNT(*) FROM Establecimiento e
                    INNER JOIN UsuarioEstablecimiento ue ON e.idEstablecimiento = ue.idEstablecimiento
                    WHERE e.establecimiento = :p_establecimiento AND ue.idUsuario = :p_idUsuario
                """)
                result = db.session.execute(query, {
                    'p_establecimiento': establecimiento,
                    'p_idUsuario': id_usuario
                })
            
            count = result.fetchone()[0]
            return count
            
        except Exception as e:
            raise Exception(f"Error al contar establecimientos por nombre: {str(e)}")
    
    @staticmethod
    def listar_por_usuario(id_usuario):
        try:
            query = text("CALL listarEstablecimientosDeUsuario(:p_idUsuario)")
            result = db.session.execute(query, {'p_idUsuario': id_usuario})
            
            establecimientos = []
            for row in result:
                establecimientos.append({
                    'idEstablecimiento': row[0],
                    'establecimiento': row[1],
                    'direccion': row[2],
                    'horaApertura': EstablecimientoDAO._format_time_for_display(row[3]),
                    'horaCierre': EstablecimientoDAO._format_time_for_display(row[4])
                })
            
            return establecimientos
            
        except Exception as e:
            raise Exception(f"Error al listar establecimientos de usuario: {str(e)}")
    
    @staticmethod
    def _verificar_propiedad(id_establecimiento, id_usuario):
        try:
            query = text("""
                SELECT COUNT(*) FROM UsuarioEstablecimiento 
                WHERE idEstablecimiento = :p_idEstablecimiento AND idUsuario = :p_idUsuario
            """)
            result = db.session.execute(query, {
                'p_idEstablecimiento': id_establecimiento,
                'p_idUsuario': id_usuario
            })
            count = result.fetchone()[0]
            return count > 0
            
        except Exception as e:
            raise Exception(f"Error al verificar propiedad del establecimiento: {str(e)}")
    
    @staticmethod
    def _format_time_for_display(time_obj):
        if time_obj is None:
            return ""
        
        if hasattr(time_obj, 'total_seconds'):
            total_seconds = int(time_obj.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours:02d}:{minutes:02d}"
        
        if hasattr(time_obj, 'hour'):
            return f"{time_obj.hour:02d}:{time_obj.minute:02d}"
        
        if isinstance(time_obj, str):
            if len(time_obj) > 5:
                time_obj = time_obj[:5]
            return time_obj
        
        return str(time_obj)
    
    @staticmethod
    def obtener_info_por_id(id_establecimiento):
        try:
            query = text("CALL usp_obtenerInfoDeEstablecimientoPorId(:p_idEstablecimiento)")
            result = db.session.execute(query, {'p_idEstablecimiento': id_establecimiento})
            row = result.fetchone()
            
            if row:
                return {
                    'idEstablecimiento': row[0],
                    'establecimiento': row[1],
                    'direccion': row[2],
                    'horaApertura': row[3],
                    'horaCierre': row[4]
                }
            return None
            
        except Exception as e:
            raise Exception(f"Error al obtener información del establecimiento: {str(e)}")
    
    @staticmethod
    def listar_establecimientos():
        try:
            query = text("CALL listarEstablecimientos()")
            result = db.session.execute(query)
            return [dict(row) for row in result]
            
        except Exception as e:
            raise Exception(f"Error al listar establecimientos: {str(e)}")