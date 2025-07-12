from app.dao.vendedorDAO import VendedorDAO
from app.dao.establecimientoDAO import EstablecimientoDAO
from app.utils.validaciones import validate_required_fields

class ServicioVendedor:
    
    @staticmethod
    def crear_vendedor(vendedor, valoracion, id_establecimiento, id_usuario):
        try:
            if not validate_required_fields([vendedor, valoracion, id_establecimiento]):
                return {
                    'success': False,
                    'message': 'Todos los campos son obligatorios'
                }
            
            if len(vendedor.strip()) < 3 or len(vendedor.strip()) > 50:
                return {
                    'success': False,
                    'message': 'El nombre del vendedor debe tener entre 3 y 50 caracteres'
                }
            
            try:
                valoracion_float = float(valoracion)
                if valoracion_float < 0 or valoracion_float > 10:
                    return {
                        'success': False,
                        'message': 'La valoración debe estar entre 0 y 10'
                    }
            except ValueError:
                return {
                    'success': False,
                    'message': 'La valoración debe ser un número válido'
                }
            
            if not EstablecimientoDAO._verificar_propiedad(id_establecimiento, id_usuario):
                return {
                    'success': False,
                    'message': 'El establecimiento seleccionado no te pertenece'
                }
            
            id_vendedor = VendedorDAO.crear_vendedor(vendedor.strip(), valoracion_float)
            
            VendedorDAO.crear_relacion_usuario_establecimiento(
                id_vendedor, id_establecimiento, id_usuario
            )
            
            return {
                'success': True,
                'message': 'Vendedor creado exitosamente'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def listar_vendedores_usuario(id_usuario):
        try:
            vendedores = VendedorDAO.listar_vendedores_por_usuario(id_usuario)
            
            return {
                'success': True,
                'vendedores': vendedores
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'vendedores': []
            }
    
    @staticmethod
    def obtener_vendedor(id_vendedor):
        try:
            vendedor = VendedorDAO.obtener_vendedor_por_id(id_vendedor)
            
            if not vendedor:
                return {
                    'success': False,
                    'message': 'Vendedor no encontrado'
                }
            
            return {
                'success': True,
                'vendedor': vendedor
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }