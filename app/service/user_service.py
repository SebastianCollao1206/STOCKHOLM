from app.dao.userDAO import UsuarioDAO
from app.utils.validaciones import validate_email, validate_password
from werkzeug.security import check_password_hash

class ServicioUsuario:
    
    @staticmethod
    def registrar_usuario(usuario, correo, clave):
        try:
            if not usuario or not correo or not clave:
                return {
                    'success': False,
                    'message': 'Todos los campos son obligatorios'
                }
            
            if not validate_email(correo):
                return {
                    'success': False,
                    'message': 'Por favor ingresa un correo electrónico válido'
                }
            
            if not validate_password(clave):
                return {
                    'success': False,
                    'message': 'La contraseña debe tener al menos 6 caracteres'
                }
            
            if len(usuario) < 3 or len(usuario) > 30:
                return {
                    'success': False,
                    'message': 'El nombre de usuario debe tener entre 3 y 30 caracteres'
                }
            
            if UsuarioDAO.verificar_correo_existe(correo):
                return {
                    'success': False,
                    'message': 'El correo electrónico ya está registrado'
                }
            
            UsuarioDAO.crear_usuario(usuario, correo, clave)
            
            return {
                'success': True,
                'message': 'Usuario registrado exitosamente. Ya puedes iniciar sesión'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def autenticar_usuario_por_correo(correo, clave):
        try:
            if not correo or not clave:
                return {
                    'success': False,
                    'message': 'Correo y contraseña son obligatorios'
                }
            
            if not validate_email(correo):
                return {
                    'success': False,
                    'message': 'Por favor ingresa un correo electrónico válido'
                }
            
            id_usuario = UsuarioDAO.obtener_id_por_correo(correo)
            
            if not id_usuario:
                return {
                    'success': False,
                    'message': 'Correo o contraseña incorrectos'
                }
            
            hash_almacenado = UsuarioDAO.obtener_hash_usuario_por_id(id_usuario)
            if not hash_almacenado:
                return {
                    'success': False,
                    'message': 'Error al verificar credenciales'
                }
            
            if not check_password_hash(hash_almacenado, clave):
                return {
                    'success': False,
                    'message': 'Correo o contraseña incorrectos'
                }
            
            info_usuario = UsuarioDAO.obtener_info_usuario_por_id(id_usuario)
            
            return {
                'success': True,
                'user': info_usuario,
                'message': 'Autenticación exitosa'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': 'Error en el servidor. Intenta nuevamente'
            }