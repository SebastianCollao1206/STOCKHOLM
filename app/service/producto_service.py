from app.dao.productoDAO import ProductoDAO
from app.utils.validaciones import validate_required_fields

class ServicioProducto:
    
    @staticmethod
    def crear_producto(id_categoria, nombre_producto, descripcion, id_marca, valoracion, imagen=None):
        try:
            if not validate_required_fields([id_categoria, nombre_producto, descripcion, id_marca, valoracion]):
                return {
                    'success': False,
                    'message': 'Todos los campos son obligatorios'
                }
            
            nombre_producto = nombre_producto.strip()
            descripcion = descripcion.strip()
            
            if len(nombre_producto) < 2 or len(nombre_producto) > 50:
                return {
                    'success': False,
                    'message': 'El nombre del producto debe tener entre 2 y 50 caracteres'
                }
            
            if len(descripcion) < 2 or len(descripcion) > 50:
                return {
                    'success': False,
                    'message': 'La descripción debe tener entre 2 y 50 caracteres'
                }
            
            try:
                valoracion = float(valoracion)
                if valoracion < 1 or valoracion > 10:
                    return {
                        'success': False,
                        'message': 'La valoración debe estar entre 1 y 10'
                    }
            except (ValueError, TypeError):
                return {
                    'success': False,
                    'message': 'La valoración debe ser un número válido'
                }
            
            try:
                id_categoria = int(id_categoria)
                id_marca = int(id_marca)
            except (ValueError, TypeError):
                return {
                    'success': False,
                    'message': 'Los IDs de categoría y marca deben ser números válidos'
                }
            
            cantidad_existente = ProductoDAO.contar_producto_por_nombre(nombre_producto)
            if cantidad_existente > 0:
                return {
                    'success': False,
                    'message': 'Ya existe un producto con este nombre'
                }
            
            id_producto = ProductoDAO.crear_producto(
                id_categoria=id_categoria,
                nombre_producto=nombre_producto,
                descripcion=descripcion,
                id_marca=id_marca,
                precio=None,  
                valoracion=valoracion,
                imagen=imagen
            )
            
            return {
                'success': True,
                'message': 'Producto creado exitosamente',
                'id_producto': id_producto
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def listar_productos():
        try:
            productos = ProductoDAO.listar_productos()
            
            return {
                'success': True,
                'productos': productos
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'productos': []
            }
    
    @staticmethod
    def obtener_producto(id_producto):
        try:
            producto = ProductoDAO.obtener_producto_por_id(id_producto)
            
            if not producto:
                return {
                    'success': False,
                    'message': 'Producto no encontrado'
                }
            
            return {
                'success': True,
                'producto': producto
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def buscar_producto_por_nombre(nombre_producto):
        try:
            id_producto = ProductoDAO.obtener_id_producto_por_nombre(nombre_producto)
            
            if not id_producto:
                return {
                    'success': False,
                    'message': 'Producto no encontrado'
                }
            
            return {
                'success': True,
                'id_producto': id_producto
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def listar_productos_de_usuario(id_usuario):
        try:
            productos = ProductoDAO.listar_productos_de_usuario(id_usuario)
            
            return {
                'success': True,
                'productos': productos
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'productos': []
            }
    
    @staticmethod
    def listar_usuario_productos_de_usuario(id_usuario):
        try:
            productos = ProductoDAO.listar_usuario_productos_de_usuario(id_usuario)
            
            return {
                'success': True,
                'productos': productos
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'productos': []
            }