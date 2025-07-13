from app.config.connection import db
from sqlalchemy import text

class NotificacionDAO:
    
    @staticmethod
    def obtener_notificaciones_por_usuario(id_usuario):
        try:
            query = text("""
                SELECT n.idNotificacion, n.titulo, n.tipo, n.descripcion, 
                       n.fechaNoti, n.estado
                FROM Notificacion n
                WHERE n.idUsuario = :id_usuario
                ORDER BY n.fechaNoti DESC
            """)
            result = db.session.execute(query, {'id_usuario': id_usuario})
            
            notificaciones = []
            for row in result:
                notificaciones.append({
                    'idNotificacion': row[0],
                    'titulo': row[1],
                    'tipo': row[2],
                    'descripcion': row[3],
                    'fechaNoti': row[4],
                    'estado': row[5]
                })
            
            return notificaciones
            
        except Exception as e:
            raise Exception(f"Error al obtener notificaciones: {str(e)}")
    
    @staticmethod
    def contar_notificaciones_no_leidas(id_usuario):
        try:
            query = text("""
                SELECT COUNT(*) 
                FROM Notificacion 
                WHERE idUsuario = :id_usuario AND estado = 'N'
            """)
            result = db.session.execute(query, {'id_usuario': id_usuario})
            return result.fetchone()[0]
            
        except Exception as e:
            raise Exception(f"Error al contar notificaciones: {str(e)}")
    
    @staticmethod
    def marcar_como_leida(id_notificacion):
        try:
            query = text("""
                UPDATE Notificacion 
                SET estado = 'L' 
                WHERE idNotificacion = :id_notificacion
            """)
            db.session.execute(query, {'id_notificacion': id_notificacion})
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al marcar notificación como leída: {str(e)}")
    
    @staticmethod
    def marcar_todas_como_leidas(id_usuario):
        try:
            query = text("""
                UPDATE Notificacion 
                SET estado = 'L' 
                WHERE idUsuario = :id_usuario AND estado = 'N'
            """)
            db.session.execute(query, {'id_usuario': id_usuario})
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al marcar todas las notificaciones como leídas: {str(e)}")
        
    