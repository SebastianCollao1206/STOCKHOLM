from app.config.connection import db
from sqlalchemy import text

class ProductoDAO:
    @staticmethod
    def crear_producto(id_categoria, nombre_producto, descripcion, id_marca, precio, valoracion, imagen):
        try:
            query = text("CALL usp_nuevoProducto(:p_idCategoria, :p_nombreProducto, :p_descripcion, :p_idMarca, :p_precio, :p_valoracion, :p_imagen)")
            db.session.execute(query, {
                'p_idCategoria': id_categoria,
                'p_nombreProducto': nombre_producto,
                'p_descripcion': descripcion,
                'p_idMarca': id_marca,
                'p_precio': precio,
                'p_valoracion': valoracion,
                'p_imagen': imagen
            })
            
            id_producto = db.session.execute(text("SELECT LAST_INSERT_ID()")).fetchone()[0]
            db.session.commit()
            return id_producto
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error al crear producto: {str(e)}")
    
    @staticmethod
    def listar_productos():
        try:
            query = text("CALL usp_listarProductos()")
            result = db.session.execute(query)
            
            productos = []
            for row in result:
                productos.append({
                    'idProducto': row[0],
                    'idCategoria': row[1],
                    'nombreProducto': row[2],
                    'descripcion': row[3],
                    'idMarca': row[4],
                    'precio': row[5],
                    'valoracion': row[6],
                    'imagen': row[7]
                })
            
            return productos
            
        except Exception as e:
            raise Exception(f"Error al listar productos: {str(e)}")
    
    @staticmethod
    def obtener_producto_por_id(id_producto):
        try:
            query = text("CALL usp_obtenerInfoDeProductoPorId(:p_idProducto)")
            result = db.session.execute(query, {'p_idProducto': id_producto})
            row = result.fetchone()
            
            if row:
                return {
                    'idProducto': row[0],
                    'idCategoria': row[1],
                    'nombreProducto': row[2],
                    'descripcion': row[3],
                    'idMarca': row[4],
                    'precio': row[5],
                    'valoracion': row[6],
                    'imagen': row[7]
                }
            return None
            
        except Exception as e:
            raise Exception(f"Error al obtener información del producto: {str(e)}")
    
    @staticmethod
    def obtener_id_producto_por_nombre(nombre_producto):
        try:
            query = text("CALL usp_obtenerIdProductoPorNombre(:p_nombreProducto)")
            result = db.session.execute(query, {'p_nombreProducto': nombre_producto})
            row = result.fetchone()
            
            if row:
                return row[0]
            return None
            
        except Exception as e:
            raise Exception(f"Error al obtener ID de producto por nombre: {str(e)}")
    
    @staticmethod
    def contar_producto_por_nombre(nombre_producto):
        try:
            query = text("CALL usp_contarProductoPorNombre(:p_nombreProducto)")
            result = db.session.execute(query, {'p_nombreProducto': nombre_producto})
            row = result.fetchone()
            
            return row[0] if row else 0
            
        except Exception as e:
            raise Exception(f"Error al contar producto por nombre: {str(e)}")
    
    @staticmethod
    def listar_productos_de_usuario(id_usuario):
        try:
            query = text("CALL listarProductosDeUsuario(:p_idUsuario)")
            result = db.session.execute(query, {'p_idUsuario': id_usuario})
            
            productos = []
            for row in result:
                productos.append({
                    'idProducto': row[0],
                    'idCategoria': row[1],
                    'nombreProducto': row[2],
                    'descripcion': row[3],
                    'idMarca': row[4],
                    'precio': row[5],
                    'valoracion': row[6],
                    'imagen': row[7]
                })
            
            return productos
            
        except Exception as e:
            raise Exception(f"Error al listar productos de usuario: {str(e)}")
    
    @staticmethod
    def listar_usuario_productos_de_usuario(id_usuario):
        try:
            query = text("CALL listarUsuarioProductosDeUsuario(:p_idUsuario)")
            result = db.session.execute(query, {'p_idUsuario': id_usuario})
            
            productos = []
            for row in result:
                productos.append({
                    'idUsuarioProducto': row[0],
                    'idUsuario': row[1],
                    'idProducto': row[2],
                    'nombreProducto': row[3],
                    'descripcion': row[4],
                    'precio': row[5],
                    'valoracion': row[6],
                    'imagen': row[7]
                })
            
            return productos
            
        except Exception as e:
            raise Exception(f"Error al listar usuario productos de usuario: {str(e)}")
        
    @staticmethod
    def listar_inventario_de_usuario(id_usuario):
        try:
            query = text("CALL usp_listarInventarioDeUsuario(:p_idUsuario)")
            result = db.session.execute(query, {'p_idUsuario': id_usuario})
            
            inventario = []
            for row in result:
                inventario.append({
                    'nombre_producto': row[0],
                    'descripcion': row[1],
                    'fecha_vencimiento': row[2],
                    'stock': row[3]
                })
            
            return inventario
            
        except Exception as e:
            raise Exception(f"Error al listar inventario de usuario: {str(e)}")

    @staticmethod
    def listar_productos_comprados_por_usuario(id_usuario):
        try:
            query = text("CALL usp_listarProductosCompradosPorUsuario(:p_idUsuario)")
            result = db.session.execute(query, {'p_idUsuario': id_usuario})
            
            productos = []
            for row in result:
                productos.append({
                    'nombre': row[0],
                    'descripcion': row[1],
                    'categoria': row[2],
                    'marca': row[3],
                    'valoracion_producto': row[4],
                    'precio': row[5],
                    'imagen': row[6]
                })
            
            return productos
            
        except Exception as e:
            raise Exception(f"Error al listar productos comprados por usuario: {str(e)}")