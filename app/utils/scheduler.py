from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.config.connection import db
from sqlalchemy import text
import logging
import atexit

logger = logging.getLogger('notifications')

class NotificacionScheduler:
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        
        atexit.register(lambda: self.scheduler.shutdown())
    
    def programar_notificaciones_vencimiento(self):
        try:
            if self.scheduler.get_job('notificaciones_vencimiento'):
                self.scheduler.remove_job('notificaciones_vencimiento')
            
            self.scheduler.add_job(
                func=self._ejecutar_notificaciones_vencimiento,
                trigger=CronTrigger(hour=7, minute=0), 
                id='notificaciones_vencimiento',
                name='Notificaciones de productos por vencer',
                replace_existing=True
            )
            
            logger.info("Scheduler de notificaciones programado para ejecutarse diariamente a las 7:00 AM")
            
        except Exception as e:
            logger.error(f"Error crítico al programar scheduler: {str(e)}")
    
    def _ejecutar_notificaciones_vencimiento(self):
        try:
            logger.info("Iniciando proceso automático de notificaciones de vencimiento")
            
            query_usuarios = text("SELECT idUsuario FROM Usuario")
            usuarios = db.session.execute(query_usuarios).fetchall()
            
            for usuario in usuarios:
                id_usuario = usuario[0]
                
                query_procedimiento = text("""
                    CALL usp_notificarProductosPorVencerParaUsuario(:id_usuario, :dias)
                """)
                
                db.session.execute(query_procedimiento, {
                    'id_usuario': id_usuario,
                    'dias': 3
                })
            
            db.session.commit()
            
            logger.info(f"Proceso de notificaciones completado exitosamente para {len(usuarios)} usuarios")
            
        except Exception as e:
            logger.error(f"Error crítico en proceso de notificaciones: {str(e)}")
            db.session.rollback()
    
    def ejecutar_ahora(self):
        logger.info("Ejecutando proceso de notificaciones manualmente")
        self._ejecutar_notificaciones_vencimiento()
    
    def detener(self):
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler de notificaciones detenido correctamente")

scheduler_instance = None

def inicializar_scheduler():
    global scheduler_instance
    if scheduler_instance is None:
        logger.info("Inicializando scheduler de notificaciones")
        scheduler_instance = NotificacionScheduler()
        scheduler_instance.programar_notificaciones_vencimiento()
    return scheduler_instance

def obtener_scheduler():
    return scheduler_instance