from app.config.connection import db
from sqlalchemy import text

class ReporteDAO:
    @staticmethod
    def obtener_vendedores_mejor_valorados(id_usuario):
        try:
            query = text("CALL usp_estadisticaVendedoresMejorValoradosDeUsuarioId(:id_usuario)")
            result = db.session.execute(query, {'id_usuario': id_usuario})
            
            vendedores = []
            for row in result:
                vendedores.append({
                    'vendedor': row[0],
                    'valoracionProm': float(row[1])
                })
            
            return vendedores[:5]  
            
        except Exception as e:
            raise Exception(f"Error al obtener vendedores mejor valorados: {str(e)}")
    
    @staticmethod
    def obtener_marcas_mas_compradas(id_usuario):
        try:
            query = text("CALL usp_estadisticaMarcasMasCompradasDeUsuarioId(:id_usuario)")
            result = db.session.execute(query, {'id_usuario': id_usuario})
            
            marcas = []
            for row in result:
                marcas.append({
                    'marca': row[0],
                    'cantidadComprada': int(row[1])
                })
            
            return marcas[:5]  
            
        except Exception as e:
            raise Exception(f"Error al obtener marcas más compradas: {str(e)}")
    
    @staticmethod
    def obtener_productos_mejor_valorados(id_usuario):
        try:
            query = text("CALL usp_estadisticaProductosMejorValoradosDeUsuarioId(:id_usuario)")
            result = db.session.execute(query, {'id_usuario': id_usuario})
            
            productos = []
            for row in result:
                productos.append({
                    'nombreProducto': row[0],
                    'valoracion': float(row[1])
                })
            
            return productos[:5]  
            
        except Exception as e:
            raise Exception(f"Error al obtener productos mejor valorados: {str(e)}")
    
    @staticmethod
    def obtener_productos_mas_comprados(id_usuario):
        try:
            query = text("CALL usp_estadisticaProductosMasCompradosPorUsuarioId(:id_usuario)")
            result = db.session.execute(query, {'id_usuario': id_usuario})
            
            productos = []
            for row in result:
                productos.append({
                    'idProducto': int(row[0]),
                    'nombreProducto': row[1],
                    'marca': row[2],
                    'categoria': row[3],
                    'totalCantidadComprada': int(row[4]),
                    'numeroCompras': int(row[5]),
                    'precioPromedio': float(row[6]),
                    'totalGastado': float(row[7])
                })
            
            return productos 
            
        except Exception as e:
            raise Exception(f"Error al obtener productos más comprados: {str(e)}")
    
    @staticmethod
    def obtener_compras_mensuales(id_usuario, año):
        try:
            query = text("CALL usp_estadisticaComprasMensualesPorAñoDeUsuario(:id_usuario, :año)")
            result = db.session.execute(query, {'id_usuario': id_usuario, 'año': año})
            
            compras_mensuales = []
            for row in result:
                compras_mensuales.append({
                    'numeroMes': int(row[0]),
                    'nombreMes': row[1],
                    'totalCompras': int(row[2]),
                    'montoTotal': float(row[3]),
                    'cantidadProductos': int(row[4])
                })
            
            return compras_mensuales
            
        except Exception as e:
            raise Exception(f"Error al obtener compras mensuales: {str(e)}")