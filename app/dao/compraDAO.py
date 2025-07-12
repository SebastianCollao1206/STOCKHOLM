from app.config.connection import db
from sqlalchemy import text

class CompraDAO:
    @staticmethod
    def crear_usuario_producto(id_usuario, id_producto, cantidad_a_agregar):
        try:
            
            query_buscar = text("""
                SELECT idUsuarioProducto, stock FROM UsuarioProducto 
                WHERE idUsuario = :p_idUsuario AND idProducto = :p_idProducto
            """)
            result = db.session.execute(query_buscar, {
                'p_idUsuario': id_usuario,
                'p_idProducto': id_producto
            })
            row = result.fetchone()
            
            if row:
                id_usuario_producto = row[0]
                stock_actual = row[1] or 0 
                stock_actual = float(stock_actual)
                nuevo_stock = stock_actual + cantidad_a_agregar
                
                query_actualizar = text("CALL usp_actualizarUsuarioProducto(:p_idUsuarioProducto, :p_idUsuario, :p_idProducto, :p_stock)")
                db.session.execute(query_actualizar, {
                    'p_idUsuarioProducto': id_usuario_producto,
                    'p_idUsuario': None,  
                    'p_idProducto': None, 
                    'p_stock': nuevo_stock
                })
                
                return id_usuario_producto
            else:
                query_crear = text("CALL usp_nuevoUsuarioProducto(:p_idUsuario, :p_idProducto, :p_stock)")
                db.session.execute(query_crear, {
                    'p_idUsuario': id_usuario,
                    'p_idProducto': id_producto,
                    'p_stock': cantidad_a_agregar
                })
                id_usuario_producto = db.session.execute(text("SELECT LAST_INSERT_ID()")).fetchone()[0]
                return id_usuario_producto
                
        except Exception as e:
            raise Exception(f"Error al crear/actualizar usuario producto: {str(e)}")
    
    @staticmethod
    def crear_compra(id_usuario_establecimiento, fecha_compra, total):
        try:
            query = text("CALL usp_nuevaCompra(:p_idUsuarioEstablecimiento, :p_fechaCompra, :p_total)")
            db.session.execute(query, {
                'p_idUsuarioEstablecimiento': id_usuario_establecimiento,
                'p_fechaCompra': fecha_compra,
                'p_total': total
            })
            id_compra = db.session.execute(text("SELECT LAST_INSERT_ID()")).fetchone()[0]
            return id_compra
        except Exception as e:
            raise Exception(f"Error al crear compra: {str(e)}")
    
    @staticmethod
    def crear_detalle(id_compra, id_usuario_producto, precio_detalle, cantidad, descuento, subtotal, fecha_vencimiento):
        try:
            query = text("CALL usp_nuevoDetalle(:p_idCompra, :p_idUsuarioProducto, :p_precioDetalle, :p_cantidad, :p_descuento, :p_subtotal, :p_fechaVencimiento, :p_restante, :p_fechaConsumo, :p_tipoConsumo, :p_desperdiciado)")
            db.session.execute(query, {
                'p_idCompra': id_compra,
                'p_idUsuarioProducto': id_usuario_producto,
                'p_precioDetalle': precio_detalle,
                'p_cantidad': cantidad,
                'p_descuento': descuento,
                'p_subtotal': subtotal,
                'p_fechaVencimiento': fecha_vencimiento,
                'p_restante': None,
                'p_fechaConsumo': None,
                'p_tipoConsumo': None,
                'p_desperdiciado': None
            })
            return True
        except Exception as e:
            raise Exception(f"Error al crear detalle: {str(e)}")
    
    @staticmethod
    def obtener_usuario_establecimiento_por_vendedor(id_vendedor, id_usuario):
        try:
            query = text("""
                SELECT idUsuarioEstablecimiento FROM UsuarioEstablecimiento 
                WHERE idVendedor = :p_idVendedor AND idUsuario = :p_idUsuario
            """)
            result = db.session.execute(query, {
                'p_idVendedor': id_vendedor,
                'p_idUsuario': id_usuario
            })
            row = result.fetchone()
            return row[0] if row else None
        except Exception as e:
            raise Exception(f"Error al obtener usuario establecimiento por vendedor: {str(e)}")
    
    @staticmethod
    def obtener_usuario_establecimiento_por_establecimiento(id_establecimiento, id_usuario):
        try:
            query = text("""
                SELECT idUsuarioEstablecimiento FROM UsuarioEstablecimiento 
                WHERE idEstablecimiento = :p_idEstablecimiento AND idUsuario = :p_idUsuario
            """)
            result = db.session.execute(query, {
                'p_idEstablecimiento': id_establecimiento,
                'p_idUsuario': id_usuario
            })
            row = result.fetchone()
            return row[0] if row else None
        except Exception as e:
            raise Exception(f"Error al obtener usuario establecimiento por establecimiento: {str(e)}")
    
    @staticmethod
    def listar_compras_de_usuario(id_usuario):
        try:
            query = text("CALL usp_listarComprasDeUsuario(:p_idUsuario)")
            result = db.session.execute(query, {'p_idUsuario': id_usuario})
            
            compras = []
            for row in result:
                compras.append({
                    'idCompra': row[0],
                    'idUsuarioEstablecimiento': row[1],
                    'fechaCompra': row[2],
                    'total': row[3],
                    'establecimiento': row[4],
                    'vendedor': row[5]
                })
            
            return compras
        except Exception as e:
            raise Exception(f"Error al listar compras de usuario: {str(e)}")
    
    @staticmethod
    def listar_detalles_de_usuario(id_usuario):
        try:
            query = text("CALL listarDetallesDeUsuario(:p_idUsuario)")
            result = db.session.execute(query, {'p_idUsuario': id_usuario})
            
            detalles = []
            for row in result:
                detalles.append({
                    'idDetalle': row[0],
                    'idCompra': row[1],
                    'idUsuarioProducto': row[2],
                    'precioDetalle': row[3],
                    'cantidad': row[4],
                    'descuento': row[5],
                    'subtotal': row[6],
                    'fechaVencimiento': row[7],
                    'restante': row[8],
                    'fechaConsumo': row[9],
                    'tipoConsumo': row[10],
                    'desperdiciado': row[11],
                    'nombreProducto': row[12],
                    'establecimiento': row[13],
                    'vendedor': row[14]
                })
            
            return detalles
        except Exception as e:
            raise Exception(f"Error al listar detalles de usuario: {str(e)}")
    
    @staticmethod
    def listar_usuario_productos_de_usuario(id_usuario):
        try:
            query = text("CALL listarUsuarioProductosDeUsuario(:p_idUsuario)")
            result = db.session.execute(query, {'p_idUsuario': id_usuario})
            
            usuario_productos = []
            for row in result:
                usuario_productos.append({
                    'idUsuarioProducto': row[0],
                    'idUsuario': row[1],
                    'idProducto': row[2],
                    'stock': row[3],
                    'nombreProducto': row[4],
                    'descripcion': row[5],
                    'precio': row[6],
                    'valoracion': row[7],
                    'imagen': row[8]
                })
            
            return usuario_productos
        except Exception as e:
            raise Exception(f"Error al listar usuario productos de usuario: {str(e)}")