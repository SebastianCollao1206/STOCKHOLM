from app.dao.categoriaDAO import CategoriaDAO

class ServicioCategoria:    
    @staticmethod
    def listar_categorias():
        try:
            categorias = CategoriaDAO.listar_categorias()
            
            return {
                'success': True,
                'categorias': categorias
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'categorias': []
            }
    
    @staticmethod
    def obtener_categoria(id_categoria):
        try:
            categoria = CategoriaDAO.obtener_categoria_por_id(id_categoria)
            
            if not categoria:
                return {
                    'success': False,
                    'message': 'Categoría no encontrada'
                }
            
            return {
                'success': True,
                'categoria': categoria
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
    
    @staticmethod
    def buscar_categoria_por_nombre(nombre_categoria):
        try:
            id_categoria = CategoriaDAO.obtener_id_categoria_por_nombre(nombre_categoria)
            
            if not id_categoria:
                return {
                    'success': False,
                    'message': 'Categoría no encontrada'
                }
            
            return {
                'success': True,
                'id_categoria': id_categoria
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e)
            }
