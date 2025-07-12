from app.dao.marcaDAO import MarcaDAO
from app.utils.validaciones import validate_required_fields

class ServicioMarca:
    
    @staticmethod
    def crear_marca(marca):
        try:
            if not validate_required_fields([marca]):
                return {
                    'success': False,
                    'message': 'El nombre de la marca es obligatorio'
                }
            
            marca_limpia = marca.strip()
            
            if len(marca_limpia) < 2 or len(marca_limpia) > 50:
                return {
                    'success': False,
                    'message': 'El nombre de la marca debe tener entre 2 y 50 caracteres'
                }
            
            cantidad_existente = MarcaDAO.contar_marca_por_nombre(marca_limpia)
            if cantidad_existente > 0:
                return {
                    'success': False,
                    'message': 'Ya existe una marca con este nombre'
                }
            
            id_marca = MarcaDAO.crear_marca(marca_limpia)
            
            return {
                'success': True,
                'message': 'Marca creada exitosamente',
                'id_marca': id_marca
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def listar_marcas():
        try:
            marcas = MarcaDAO.listar_marcas()
            
            return {
                'success': True,
                'marcas': marcas
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'marcas': []
            }
    
    @staticmethod
    def obtener_marca(id_marca):
        try:
            marca = MarcaDAO.obtener_marca_por_id(id_marca)
            
            if not marca:
                return {
                    'success': False,
                    'message': 'Marca no encontrada'
                }
            
            return {
                'success': True,
                'marca': marca
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def buscar_marca_por_nombre(nombre_marca):
        try:
            id_marca = MarcaDAO.obtener_id_marca_por_nombre(nombre_marca)
            
            if not id_marca:
                return {
                    'success': False,
                    'message': 'Marca no encontrada'
                }
            
            return {
                'success': True,
                'id_marca': id_marca
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }