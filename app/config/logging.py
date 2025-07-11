import logging
import os
from datetime import datetime

def setup_logging(app):
    
    log_dir = os.path.join(app.instance_path, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    file_handler = logging.FileHandler(
        os.path.join(log_dir, f'app_{datetime.now().strftime("%Y%m%d")}.log')
    )
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.INFO)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    console_handler.setLevel(logging.DEBUG)
    
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.DEBUG)
    
    auth_logger = logging.getLogger('auth')
    auth_logger.addHandler(file_handler)
    auth_logger.addHandler(console_handler)
    auth_logger.setLevel(logging.DEBUG)
    
    notifications_logger = logging.getLogger('notifications')
    notifications_logger.addHandler(file_handler)
    notifications_logger.addHandler(console_handler)
    notifications_logger.setLevel(logging.DEBUG)
    
    app.logger.info('Sistema de logging configurado correctamente')
    
    return app