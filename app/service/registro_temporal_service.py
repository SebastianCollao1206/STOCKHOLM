from datetime import datetime
from flask import session
from app.service.producto_service import ServicioProducto

class ServicioRegistroTemporal:
    
    @staticmethod
    def inicializar_registro():
        if 'registro_temporal' not in session:
            session['registro_temporal'] = []
    
    @staticmethod
    def agregar_producto_al_registro(producto_id, precio, cantidad, descuento, fecha_vencimiento):
        try:
            result_producto = ServicioProducto.obtener_producto(producto_id)
            if not result_producto['success']:
                return {
                    'success': False,
                    'message': 'Producto no encontrado'
                }
            
            producto = result_producto['producto']
            
            if not all([producto_id, precio, cantidad, fecha_vencimiento]):
                return {
                    'success': False,
                    'message': 'Todos los campos son obligatorios'
                }
            
            try:
                precio = float(precio)
                cantidad = float(cantidad)
                descuento = float(descuento) if descuento else 0
                
                if precio <= 0:
                    return {
                        'success': False,
                        'message': 'El precio debe ser mayor a 0'
                    }
                
                if cantidad <= 0:
                    return {
                        'success': False,
                        'message': 'La cantidad debe ser mayor a 0'
                    }
                
                if descuento < 0 or descuento > 100:
                    return {
                        'success': False,
                        'message': 'El descuento debe estar entre 0 y 100'
                    }
                
            except (ValueError, TypeError):
                return {
                    'success': False,
                    'message': 'Valores numéricos inválidos'
                }
            
            try:
                fecha_vencimiento_obj = datetime.strptime(fecha_vencimiento, '%Y-%m-%d').date()
                if fecha_vencimiento_obj <= datetime.now().date():
                    return {
                        'success': False,
                        'message': 'La fecha de vencimiento debe ser posterior a hoy'
                    }
            except ValueError:
                return {
                    'success': False,
                    'message': 'Formato de fecha inválido'
                }
            
            subtotal = (precio * cantidad) - (precio * cantidad * descuento / 100)
            
            item_registro = {
                'id_temp': len(session.get('registro_temporal', [])) + 1, 
                'producto_id': producto_id,
                'nombre_producto': producto['nombreProducto'],
                'descripcion': producto['descripcion'],
                'imagen': producto['imagen'],
                'precio': precio,
                'cantidad': cantidad,
                'descuento': descuento,
                'subtotal': round(subtotal, 2),
                'fecha_vencimiento': fecha_vencimiento,
                'restante': cantidad,  
                'fecha_agregado': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            ServicioRegistroTemporal.inicializar_registro()
            
            session['registro_temporal'].append(item_registro)
            session.modified = True
            
            print(f"[DEBUG] Producto agregado al registro temporal:")
            print(f"[DEBUG] - ID Temp: {item_registro['id_temp']}")
            print(f"[DEBUG] - Producto: {item_registro['nombre_producto']}")
            print(f"[DEBUG] - Precio: {item_registro['precio']}")
            print(f"[DEBUG] - Cantidad: {item_registro['cantidad']}")
            print(f"[DEBUG] - Subtotal: {item_registro['subtotal']}")
            print(f"[DEBUG] Total de items en registro: {len(session['registro_temporal'])}")
            
            return {
                'success': True,
                'message': 'Producto agregado al registro exitosamente',
                'item': item_registro
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al agregar producto: {str(e)}'
            }
    
    @staticmethod
    def editar_producto_del_registro(id_temp, precio, cantidad, descuento, fecha_vencimiento):
        try:
            ServicioRegistroTemporal.inicializar_registro()
            
            registro = session['registro_temporal']
            item_encontrado = None
            index = -1
            
            for i, item in enumerate(registro):
                if item['id_temp'] == id_temp:
                    item_encontrado = item
                    index = i
                    break
            
            if not item_encontrado:
                return {
                    'success': False,
                    'message': 'Producto no encontrado en el registro'
                }
            
            if not all([precio, cantidad, fecha_vencimiento]):
                return {
                    'success': False,
                    'message': 'Todos los campos son obligatorios'
                }
            
            try:
                precio = float(precio)
                cantidad = float(cantidad)
                descuento = float(descuento) if descuento else 0
                
                if precio <= 0:
                    return {
                        'success': False,
                        'message': 'El precio debe ser mayor a 0'
                    }
                
                if cantidad <= 0:
                    return {
                        'success': False,
                        'message': 'La cantidad debe ser mayor a 0'
                    }
                
                if descuento < 0 or descuento > 100:
                    return {
                        'success': False,
                        'message': 'El descuento debe estar entre 0 y 100'
                    }
                
            except (ValueError, TypeError):
                return {
                    'success': False,
                    'message': 'Valores numéricos inválidos'
                }
            
            try:
                fecha_vencimiento_obj = datetime.strptime(fecha_vencimiento, '%Y-%m-%d').date()
                if fecha_vencimiento_obj <= datetime.now().date():
                    return {
                        'success': False,
                        'message': 'La fecha de vencimiento debe ser posterior a hoy'
                    }
            except ValueError:
                return {
                    'success': False,
                    'message': 'Formato de fecha inválido'
                }
            
            subtotal = (precio * cantidad) - (precio * cantidad * descuento / 100)
            
            session['registro_temporal'][index].update({
                'precio': precio,
                'cantidad': cantidad,
                'descuento': descuento,
                'subtotal': round(subtotal, 2),
                'fecha_vencimiento': fecha_vencimiento,
                'restante': cantidad,  
                'fecha_modificado': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            
            session.modified = True
            
            print(f"[DEBUG] Producto editado en el registro temporal:")
            print(f"[DEBUG] - ID Temp: {id_temp}")
            print(f"[DEBUG] - Producto: {session['registro_temporal'][index]['nombre_producto']}")
            print(f"[DEBUG] - Precio: {session['registro_temporal'][index]['precio']}")
            print(f"[DEBUG] - Cantidad: {session['registro_temporal'][index]['cantidad']}")
            print(f"[DEBUG] - Subtotal: {session['registro_temporal'][index]['subtotal']}")
            
            return {
                'success': True,
                'message': 'Producto actualizado exitosamente',
                'item': session['registro_temporal'][index]
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al editar producto: {str(e)}'
            }
    
    @staticmethod
    def obtener_producto_del_registro(id_temp):
        try:
            ServicioRegistroTemporal.inicializar_registro()
            
            for item in session['registro_temporal']:
                if item['id_temp'] == id_temp:
                    return {
                        'success': True,
                        'item': item
                    }
            
            return {
                'success': False,
                'message': 'Producto no encontrado en el registro'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al obtener producto: {str(e)}'
            }
    
    @staticmethod
    def listar_productos_del_registro():
        try:
            ServicioRegistroTemporal.inicializar_registro()
            
            productos = session.get('registro_temporal', [])
            total_items = len(productos)
            total_general = sum(item['subtotal'] for item in productos)
            
            print(f"[DEBUG] Listado del registro temporal:")
            print(f"[DEBUG] - Total items: {total_items}")
            print(f"[DEBUG] - Total general: {total_general}")
            
            for item in productos:
                print(f"[DEBUG] - Item ID: {item['id_temp']} | Producto: {item['nombre_producto']} | Subtotal: {item['subtotal']}")
            
            return {
                'success': True,
                'productos': productos,
                'total_items': total_items,
                'total_general': round(total_general, 2)
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al listar productos: {str(e)}',
                'productos': [],
                'total_items': 0,
                'total_general': 0
            }
    
    @staticmethod
    def eliminar_producto_del_registro(id_temp):
        try:
            ServicioRegistroTemporal.inicializar_registro()
            
            registro = session['registro_temporal']
            registro_actualizado = [item for item in registro if item['id_temp'] != id_temp]
            
            if len(registro_actualizado) == len(registro):
                return {
                    'success': False,
                    'message': 'Producto no encontrado en el registro'
                }
            
            session['registro_temporal'] = registro_actualizado
            session.modified = True
            
            print(f"[DEBUG] Producto eliminado del registro temporal (ID: {id_temp})")
            print(f"[DEBUG] Total de items restantes: {len(session['registro_temporal'])}")
            
            return {
                'success': True,
                'message': 'Producto eliminado del registro exitosamente'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al eliminar producto: {str(e)}'
            }
    
    @staticmethod
    def limpiar_registro():
        try:
            session['registro_temporal'] = []
            session.modified = True
            
            print("[DEBUG] Registro temporal limpiado completamente")
            
            return {
                'success': True,
                'message': 'Registro temporal limpiado exitosamente'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al limpiar registro: {str(e)}'
            }