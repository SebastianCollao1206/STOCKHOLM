from flask import session
import logging

logger = logging.getLogger('notifications')

class Notificacion:
    @staticmethod
    def set_alert(message, alert_type='info', title=None):
        alert_data = {
            'message': message,
            'type': alert_type,
            'title': title
        }
        session['alert'] = alert_data
        logger.info(f'Alerta establecida: {alert_data}')
    
    @staticmethod
    def get_alert():
        alert = session.pop('alert', None)
        if alert:
            logger.info(f'Alerta obtenida: {alert}')
        else:
            logger.debug('No hay alertas en la sesión')
        return alert
    
    @staticmethod
    def success(message, title="¡Éxito!"):
        logger.info(f'Alerta de éxito: {title} - {message}')
        Notificacion.set_alert(message, 'success', title)
    
    @staticmethod
    def error(message, title="¡Error!"):
        logger.error(f'Alerta de error: {title} - {message}')
        Notificacion.set_alert(message, 'error', title)
    
    @staticmethod
    def warning(message, title="¡Advertencia!"):
        logger.warning(f'Alerta de advertencia: {title} - {message}')
        Notificacion.set_alert(message, 'warning', title)
    
    @staticmethod
    def info(message, title="Información"):
        logger.info(f'Alerta informativa: {title} - {message}')
        Notificacion.set_alert(message, 'info', title)