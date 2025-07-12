from app.config.connection import db
from sqlalchemy import text

class CategoriaDAO:
    @staticmethod
    def listar_categorias():
        try:
            query = text("CALL usp_listarCategorias()")
            result = db.session.execute(query)
            
            categorias = []
            for row in result:
                categorias.append({
                    'idCategoria': row[0],
                    'categoria': row[1]
                })
            
            return categorias
            
        except Exception as e:
            raise Exception(f"Error al listar categorías: {str(e)}")
    
    @staticmethod
    def obtener_categoria_por_id(id_categoria):
        try:
            query = text("CALL usp_obtenerInfoDeCategoriaPorId(:p_idCategoria)")
            result = db.session.execute(query, {'p_idCategoria': id_categoria})
            row = result.fetchone()
            
            if row:
                return {
                    'idCategoria': row[0],
                    'categoria': row[1]
                }
            return None
            
        except Exception as e:
            raise Exception(f"Error al obtener información de la categoría: {str(e)}")
    
    @staticmethod
    def obtener_id_categoria_por_nombre(categoria):
        try:
            query = text("CALL usp_obtenerIdCategoriaPorNombre(:p_categoria)")
            result = db.session.execute(query, {'p_categoria': categoria})
            row = result.fetchone()
            
            if row:
                return row[0]
            return None
            
        except Exception as e:
            raise Exception(f"Error al obtener ID de categoría por nombre: {str(e)}")
