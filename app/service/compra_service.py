from datetime import datetime
from app.dao.compraDAO import CompraDAO
from app.config.connection import db

class ServicioCompra:
    
    @staticmethod
    def guardar_compra(id_usuario, vendedor_id, establecimiento_id, fecha_compra, productos_registro):
        try:
            if vendedor_id and establecimiento_id:
                return {
                    'success': False,
                    'message': 'Solo puedes seleccionar vendedor o establecimiento, no ambos'
                }
            
            if not vendedor_id and not establecimiento_id:
                return {
                    'success': False,
                    'message': 'Debes seleccionar al menos un vendedor o establecimiento'
                }
            
            if not productos_registro:
                return {
                    'success': False,
                    'message': 'No hay productos en el registro'
                }
            
            try:
                fecha_compra_obj = datetime.strptime(fecha_compra, '%Y-%m-%d')
            except ValueError:
                return {
                    'success': False,
                    'message': 'Formato de fecha inválido'
                }
            
            id_usuario_establecimiento = None
            if vendedor_id:
                id_usuario_establecimiento = CompraDAO.obtener_usuario_establecimiento_por_vendedor(vendedor_id, id_usuario)
            elif establecimiento_id:
                id_usuario_establecimiento = CompraDAO.obtener_usuario_establecimiento_por_establecimiento(establecimiento_id, id_usuario)
            
            if not id_usuario_establecimiento:
                return {
                    'success': False,
                    'message': 'No se encontró la relación usuario-establecimiento'
                }
            
            total_compra = sum(producto['subtotal'] for producto in productos_registro)
            
            productos_usuario_producto = []
            for producto in productos_registro:
                id_usuario_producto = CompraDAO.crear_usuario_producto(
                    id_usuario=id_usuario,
                    id_producto=producto['producto_id'],
                    stock=None
                )
                productos_usuario_producto.append({
                    'id_usuario_producto': id_usuario_producto,
                    'producto_data': producto
                })
            
            id_compra = CompraDAO.crear_compra(
                id_usuario_establecimiento=id_usuario_establecimiento,
                fecha_compra=fecha_compra_obj,
                total=total_compra
            )
            
            for item in productos_usuario_producto:
                producto_data = item['producto_data']
                CompraDAO.crear_detalle(
                    id_compra=id_compra,
                    id_usuario_producto=item['id_usuario_producto'],
                    precio_detalle=producto_data['precio'],
                    cantidad=producto_data['cantidad'],
                    descuento=producto_data['descuento'],
                    subtotal=producto_data['subtotal'],
                    fecha_vencimiento=producto_data['fecha_vencimiento']
                )
            
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Compra guardada exitosamente',
                'id_compra': id_compra,
                'total': total_compra
            }
            
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'message': f'Error al guardar la compra: {str(e)}'
            }
    
    @staticmethod
    def listar_compras_usuario(id_usuario):
        try:
            compras = CompraDAO.listar_compras_de_usuario(id_usuario)
            return {
                'success': True,
                'compras': compras
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al listar compras: {str(e)}',
                'compras': []
            }
    
    @staticmethod
    def listar_detalles_usuario(id_usuario):
        try:
            detalles = CompraDAO.listar_detalles_de_usuario(id_usuario)
            return {
                'success': True,
                'detalles': detalles
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al listar detalles: {str(e)}',
                'detalles': []
            }
    
    @staticmethod
    def listar_usuario_productos_usuario(id_usuario):
        try:
            usuario_productos = CompraDAO.listar_usuario_productos_de_usuario(id_usuario)
            return {
                'success': True,
                'usuario_productos': usuario_productos
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al listar usuario productos: {str(e)}',
                'usuario_productos': []
            }