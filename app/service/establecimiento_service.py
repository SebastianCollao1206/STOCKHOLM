from app.dao.establecimientoDAO import EstablecimientoDAO
from app.utils.validaciones import validate_time_format, validate_required_fields
from datetime import datetime

class ServicioEstablecimiento:
    
    @staticmethod
    def crear_establecimiento(establecimiento, direccion, hora_apertura, hora_cierre, id_usuario):
        try:
            if not validate_required_fields([establecimiento, direccion, hora_apertura, hora_cierre]):
                return {
                    'success': False,
                    'message': 'Todos los campos son obligatorios'
                }
            
            if len(establecimiento.strip()) < 3 or len(establecimiento.strip()) > 100:
                return {
                    'success': False,
                    'message': 'El nombre del establecimiento debe tener entre 3 y 100 caracteres'
                }
            
            if len(direccion.strip()) < 5 or len(direccion.strip()) > 150:
                return {
                    'success': False,
                    'message': 'La dirección debe tener entre 5 y 150 caracteres'
                }
            
            if not validate_time_format(hora_apertura) or not validate_time_format(hora_cierre):
                return {
                    'success': False,
                    'message': 'Las horas deben tener un formato válido (HH:MM)'
                }
            
            apertura = datetime.strptime(hora_apertura, '%H:%M').time()
            cierre = datetime.strptime(hora_cierre, '%H:%M').time()
            
            if apertura >= cierre:
                return {
                    'success': False,
                    'message': 'La hora de apertura debe ser anterior a la hora de cierre'
                }
            
            if EstablecimientoDAO.contar_por_nombre(establecimiento, id_usuario) > 0:
                return {
                    'success': False,
                    'message': 'Ya tienes un establecimiento con ese nombre'
                }
            
            EstablecimientoDAO.crear_establecimiento(
                establecimiento,
                direccion,
                hora_apertura,
                hora_cierre,
                id_usuario
            )
            
            return {
                'success': True,
                'message': 'Establecimiento creado exitosamente'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def actualizar_establecimiento(id_establecimiento, establecimiento, direccion, hora_apertura, hora_cierre, id_usuario):
        try:
            establecimiento_actual = EstablecimientoDAO.obtener_establecimiento_por_id(id_establecimiento, id_usuario)
            if not establecimiento_actual:
                return {
                    'success': False,
                    'message': 'El establecimiento no existe o no tienes permisos para editarlo'
                }
            
            if not validate_required_fields([establecimiento, direccion, hora_apertura, hora_cierre]):
                return {
                    'success': False,
                    'message': 'Todos los campos son obligatorios'
                }
            
            if len(establecimiento.strip()) < 3 or len(establecimiento.strip()) > 100:
                return {
                    'success': False,
                    'message': 'El nombre del establecimiento debe tener entre 3 y 100 caracteres'
                }
            
            if len(direccion.strip()) < 5 or len(direccion.strip()) > 150:
                return {
                    'success': False,
                    'message': 'La dirección debe tener entre 5 y 150 caracteres'
                }
            
            if not validate_time_format(hora_apertura) or not validate_time_format(hora_cierre):
                return {
                    'success': False,
                    'message': 'Las horas deben tener un formato válido (HH:MM)'
                }
            
            apertura = datetime.strptime(hora_apertura, '%H:%M').time()
            cierre = datetime.strptime(hora_cierre, '%H:%M').time()
            
            if apertura >= cierre:
                return {
                    'success': False,
                    'message': 'La hora de apertura debe ser anterior a la hora de cierre'
                }
            
            if establecimiento.strip() != establecimiento_actual['establecimiento']:
                if EstablecimientoDAO.contar_por_nombre(establecimiento, id_usuario, id_establecimiento) > 0:
                    return {
                        'success': False,
                        'message': 'Ya tienes otro establecimiento con ese nombre'
                    }
            
            EstablecimientoDAO.actualizar_establecimiento(
                id_establecimiento,
                establecimiento,
                direccion,
                hora_apertura,
                hora_cierre,
                id_usuario
            )
            
            return {
                'success': True,
                'message': 'Establecimiento actualizado exitosamente'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def obtener_establecimiento(id_establecimiento, id_usuario):
        try:
            establecimiento = EstablecimientoDAO.obtener_establecimiento_por_id(id_establecimiento, id_usuario)
            
            if not establecimiento:
                return {
                    'success': False,
                    'message': 'Establecimiento no encontrado o no tienes permisos para verlo'
                }
            
            return {
                'success': True,
                'establecimiento': establecimiento
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def listar_establecimientos_usuario(id_usuario):
        try:
            establecimientos = EstablecimientoDAO.listar_por_usuario(id_usuario)
            
            return {
                'success': True,
                'establecimientos': establecimientos
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'establecimientos': []
            }
    