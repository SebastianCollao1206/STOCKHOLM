from app.dao.notificacionDAO import NotificacionDAO
from datetime import datetime

class ServicioNotificacion:
    
    @staticmethod
    def obtener_notificaciones_usuario(id_usuario):
        try:
            notificaciones = NotificacionDAO.obtener_notificaciones_por_usuario(id_usuario)
            
            for notificacion in notificaciones:
                notificacion['fechaNoti'] = notificacion['fechaNoti'].strftime('%d/%m/%Y %H:%M')
                notificacion['es_nueva'] = notificacion['estado'] == 'N'
            
            return {
                'success': True,
                'notificaciones': notificaciones
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def obtener_contador_notificaciones(id_usuario):
        try:
            contador = NotificacionDAO.contar_notificaciones_no_leidas(id_usuario)
            return {
                'success': True,
                'contador': contador
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def marcar_todas_leidas(id_usuario):
        try:
            NotificacionDAO.marcar_todas_como_leidas(id_usuario)
            return {
                'success': True,
                'message': 'Todas las notificaciones han sido marcadas como leídas'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }