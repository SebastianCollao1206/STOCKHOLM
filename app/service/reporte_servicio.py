from app.dao.reporteDAO import ReporteDAO
from datetime import datetime

class ServicioReporte:
    @staticmethod
    def obtener_vendedores_mejor_valorados(id_usuario):
        try:
            vendedores = ReporteDAO.obtener_vendedores_mejor_valorados(id_usuario)
            
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
    def obtener_marcas_mas_compradas(id_usuario):
        try:
            marcas = ReporteDAO.obtener_marcas_mas_compradas(id_usuario)
            
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
    def obtener_productos_mejor_valorados(id_usuario):
        try:
            productos = ReporteDAO.obtener_productos_mejor_valorados(id_usuario)
            
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
    def obtener_productos_mas_comprados(id_usuario):
        try:
            productos = ReporteDAO.obtener_productos_mas_comprados(id_usuario)
            
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
    def obtener_compras_mensuales(id_usuario, año=None):
        try:
            if año is None:
                año = datetime.now().year
                
            compras = ReporteDAO.obtener_compras_mensuales(id_usuario, año)
            
            return {
                'success': True,
                'compras': compras,
                'año': año
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'compras': [],
                'año': año
            }
    
    @staticmethod
    def obtener_todos_los_reportes(id_usuario, año=None):
        try:
            vendedores = ServicioReporte.obtener_vendedores_mejor_valorados(id_usuario)
            marcas = ServicioReporte.obtener_marcas_mas_compradas(id_usuario)
            productos_valorados = ServicioReporte.obtener_productos_mejor_valorados(id_usuario)
            productos_comprados = ServicioReporte.obtener_productos_mas_comprados(id_usuario)
            compras_mensuales = ServicioReporte.obtener_compras_mensuales(id_usuario, año)
            
            return {
                'success': True,
                'data': {
                    'vendedores': vendedores['vendedores'],
                    'marcas': marcas['marcas'],
                    'productos_valorados': productos_valorados['productos'],
                    'productos_comprados': productos_comprados['productos'],
                    'compras_mensuales': compras_mensuales['compras'],
                    'año': compras_mensuales['año']
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
                'data': {}
            }