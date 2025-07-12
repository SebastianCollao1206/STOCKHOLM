from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.utils.auth_decorators import login_required
from app.utils.notificaciones import Notificacion
from app.service.establecimiento_service import ServicioEstablecimiento
from app.service.vendedor_service import ServicioVendedor
from app.service.marca_service import ServicioMarca
from app.service.categoria_service import ServicioCategoria
from app.service.producto_service import ServicioProducto
from app.service.registro_temporal_service import ServicioRegistroTemporal
from app.service.compra_service import ServicioCompra
from app.service.reporte_servicio import ServicioReporte

main_bp = Blueprint('main', __name__)

#REPORTES
@main_bp.route('/reportes')
@login_required
def reportes():
    try:
        user_id = session.get('user_id')
        if not user_id:
            Notificacion.error('Error de sesión')
            return redirect(url_for('auth.login'))
        año = request.args.get('año', type=int)
        
        reportes_data = ServicioReporte.obtener_todos_los_reportes(user_id, año)
        
        if reportes_data['success']:
            return render_template('main/reportes.html', 
                                 reportes=reportes_data['data'],
                                 año_actual=reportes_data['data']['año'])
        else:
            return render_template('main/reportes.html', 
                                 reportes={},
                                 año_actual=2024,
                                 error=reportes_data['message'])
        
    except Exception as e:
        return render_template('main/reportes.html', 
                             reportes={},
                             año_actual=2024,
                             error='Error interno del servidor')

@main_bp.route('/api/reportes/vendedores')
@login_required
def api_vendedores():
    try:
        user_id = session.get('user_id')
        if not user_id:
            Notificacion.error('Error de sesión')
            return redirect(url_for('auth.login'))
        result = ServicioReporte.obtener_vendedores_mejor_valorados(user_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@main_bp.route('/api/reportes/marcas')
@login_required
def api_marcas():
    try:
        user_id = session.get('user_id')
        if not user_id:
            Notificacion.error('Error de sesión')
            return redirect(url_for('auth.login'))
        result = ServicioReporte.obtener_marcas_mas_compradas(user_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@main_bp.route('/api/reportes/productos-valorados')
@login_required
def api_productos_valorados():
    try:
        user_id = session.get('user_id')
        if not user_id:
            Notificacion.error('Error de sesión')
            return redirect(url_for('auth.login'))
        result = ServicioReporte.obtener_productos_mejor_valorados(user_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@main_bp.route('/api/reportes/productos-comprados')
@login_required
def api_productos_comprados():
    try:
        user_id = session.get('user_id')
        if not user_id:
            Notificacion.error('Error de sesión')
            return redirect(url_for('auth.login'))
        result = ServicioReporte.obtener_productos_mas_comprados(user_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@main_bp.route('/api/reportes/compras-mensuales')
@login_required
def api_compras_mensuales():
    try:
        user_id = session.get('user_id')
        if not user_id:
            Notificacion.error('Error de sesión')
            return redirect(url_for('auth.login'))
        año = request.args.get('año', type=int)
        result = ServicioReporte.obtener_compras_mensuales(user_id, año)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

#VENDEDOR
@main_bp.route('/vendedor/agregar', methods=['GET', 'POST'])
@login_required
def vendedor_agregar():
    try:
        user_id = session.get('user_id')
        if not user_id:
            Notificacion.error('Error de sesión')
            return redirect(url_for('auth.login'))
        
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            valoracion = request.form.get('valoracion')
            id_establecimiento = request.form.get('establecimiento')
            
            if not all([nombre, valoracion, id_establecimiento]):
                Notificacion.error('Todos los campos son obligatorios')
                result = ServicioEstablecimiento.listar_establecimientos_usuario(user_id)
                establecimientos = result['establecimientos'] if result['success'] else []
                return render_template('main/agregar_vendedor.html', establecimientos=establecimientos)
            
            result = ServicioVendedor.crear_vendedor(
                nombre, valoracion, int(id_establecimiento), user_id
            )
            
            if result['success']:
                Notificacion.success(result['message'])
                return redirect(url_for('main.vendedor_agregar'))
            else:
                Notificacion.error(result['message'])
                result_est = ServicioEstablecimiento.listar_establecimientos_usuario(user_id)
                establecimientos = result_est['establecimientos'] if result_est['success'] else []
                return render_template('main/agregar_vendedor.html', establecimientos=establecimientos)
        
        result = ServicioEstablecimiento.listar_establecimientos_usuario(user_id)
        
        if not result['success']:
            Notificacion.error('Error al cargar los establecimientos')
            establecimientos = []
        else:
            establecimientos = result['establecimientos']
        
        return render_template('main/agregar_vendedor.html', establecimientos=establecimientos)
        
    except Exception as e:
        Notificacion.error('Error interno del servidor')
        return render_template('main/agregar_vendedor.html', establecimientos=[])

#PRESENTACION
@main_bp.route('/presentacion/agregar', methods=['GET', 'POST'])
@login_required
def producto_agregar():
    try:
        user_id = session.get('user_id')
        if not user_id:
            Notificacion.error('Error de sesión')
            return redirect(url_for('auth.login'))
        
        if request.method == 'POST':
            id_categoria = request.form.get('categoria')
            nombre_producto = request.form.get('nombre-producto')
            descripcion = request.form.get('descripcion')
            id_marca = request.form.get('marca')
            valoracion = request.form.get('valoracion')
            imagen = request.form.get('imagen')
            
            if not all([id_categoria, nombre_producto, descripcion, id_marca, valoracion]):
                Notificacion.error('Todos los campos son obligatorios')
                result_categorias = ServicioCategoria.listar_categorias()
                result_marcas = ServicioMarca.listar_marcas()
                
                categorias = result_categorias['categorias'] if result_categorias['success'] else []
                marcas = result_marcas['marcas'] if result_marcas['success'] else []
                
                return render_template('main/agregar_presentacion.html', 
                                     categorias=categorias, 
                                     marcas=marcas)
            
            result = ServicioProducto.crear_producto(
                id_categoria=id_categoria,
                nombre_producto=nombre_producto,
                descripcion=descripcion,
                id_marca=id_marca,
                valoracion=valoracion,
                imagen=imagen if imagen else None
            )
            
            if result['success']:
                Notificacion.success(result['message'])
                return redirect(url_for('main.producto_agregar'))
            else:
                Notificacion.error(result['message'])
                result_categorias = ServicioCategoria.listar_categorias()
                result_marcas = ServicioMarca.listar_marcas()
                
                categorias = result_categorias['categorias'] if result_categorias['success'] else []
                marcas = result_marcas['marcas'] if result_marcas['success'] else []
                
                return render_template('main/agregar_presentacion.html', 
                                     categorias=categorias, 
                                     marcas=marcas)
        
        result_categorias = ServicioCategoria.listar_categorias()
        result_marcas = ServicioMarca.listar_marcas()
        
        if not result_categorias['success']:
            Notificacion.error('Error al cargar las categorías')
            categorias = []
        else:
            categorias = result_categorias['categorias']
            
        if not result_marcas['success']:
            Notificacion.error('Error al cargar las marcas')
            marcas = []
        else:
            marcas = result_marcas['marcas']
        
        return render_template('main/agregar_presentacion.html', 
                             categorias=categorias, 
                             marcas=marcas)
        
    except Exception as e:
        Notificacion.error('Error interno del servidor')
        return render_template('main/agregar_presentacion.html', 
                             categorias=[], 
                             marcas=[])


#MARCA
@main_bp.route('/marca/agregar', methods=['GET', 'POST'])
@login_required
def marca_agregar():
    try:
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            
            if not nombre:
                Notificacion.error('El nombre de la marca es obligatorio')
                return render_template('main/agregar_marca.html')
            
            result = ServicioMarca.crear_marca(nombre)
            
            if result['success']:
                Notificacion.success(result['message'])
                return redirect(url_for('main.marca_agregar'))
            else:
                Notificacion.error(result['message'])
                return render_template('main/agregar_marca.html')
        
        return render_template('main/agregar_marca.html')
        
    except Exception as e:
        Notificacion.error('Error interno del servidor')
        return render_template('main/agregar_marca.html')

# #INVENTARIO
@main_bp.route('/inventario')
@login_required
def inventario():
    try:
        id_usuario = session.get('user_id')
        
        if not id_usuario:
            return render_template('main/inventario.html', inventario=[], error="Usuario no autenticado")
        
        resultado = ServicioProducto.listar_inventario_de_usuario(id_usuario)
        
        if resultado['success']:
            inventario = resultado['inventario']
        else:
            inventario = []
            
        return render_template('main/inventario.html', inventario=inventario)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return render_template('main/inventario.html', inventario=[], error=f"Error al cargar inventario: {str(e)}")

#PRODUCTOS
@main_bp.route('/productos')
@login_required
def productos():
    try:
        id_usuario = session.get('user_id')
        
        if not id_usuario:
            return render_template('main/productos.html', productos=[], error="Usuario no autenticado")
        
        resultado = ServicioProducto.listar_productos_comprados_por_usuario(id_usuario)
        
        if resultado['success']:
            productos = resultado['productos']
        else:
            productos = []
            
        return render_template('main/productos.html', productos=productos)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return render_template('main/productos.html', productos=[], error=f"Error al cargar productos: {str(e)}")

#REGISTROS
@main_bp.route('/registros')
@login_required
def registros():
    try:
        id_usuario = session.get('user_id')
        
        if not id_usuario:
            return render_template('main/registros.html', compras=[], error="Usuario no autenticado")
        
        resultado = ServicioCompra.listar_compras_usuario(id_usuario)
        
        if resultado['success']:
            compras = resultado['compras']
        else:
            compras = []
            
        return render_template('main/registros.html', compras=compras)
        
    except Exception as e:
        return render_template('main/registros.html', compras=[], error=f"Error al cargar registros: {str(e)}")

@main_bp.route('/detalle/registro/<int:id>', methods=['GET', 'POST'])
@login_required
def detalle_registro(id):
    try:
        id_usuario = session.get('user_id')
        
        if not id_usuario:
            return render_template('main/detalle_registro.html', detalles=[], error="Usuario no autenticado")
        
        resultado = ServicioCompra.listar_detalle_compra(id)
        
        if resultado['success']:
            detalles = resultado['detalles']
        else:
            detalles = []
            
        return render_template('main/detalle_registro.html', detalles=detalles)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return render_template('main/detalle_registro.html', detalles=[], error=f"Error al cargar detalle: {str(e)}")

    
@main_bp.route('/registro/agregar')
@login_required
def registro_agregar():
    try:
        user_id = session.get('user_id')
        if not user_id:
            Notificacion.error('Error de sesión')
            return redirect(url_for('auth.login'))
        
        result_registro = ServicioRegistroTemporal.listar_productos_del_registro()
        registro_productos = result_registro['productos'] if result_registro['success'] else []

        result_vendedores = ServicioVendedor.listar_vendedores_usuario(user_id)
        if not result_vendedores['success']:
            Notificacion.error('Error al cargar los vendedores')
            vendedores = []
        else:
            vendedores = result_vendedores['vendedores']

        
        result_establecimientos = ServicioEstablecimiento.listar_establecimientos_usuario(user_id)
        if not result_establecimientos['success']:
            Notificacion.error('Error al cargar los establecimientos')
            establecimientos = []
        else:
            establecimientos = result_establecimientos['establecimientos']

        return render_template(
            'main/agregar_registro.html',  
            registro_productos=registro_productos,
            total_items=result_registro.get('total_items', 0),
            total_general=result_registro.get('total_general', 0),
            vendedores=vendedores,
            establecimientos=establecimientos
        )
        
    except Exception as e:
        print(f"Error en registro_agregar: {str(e)}")
        Notificacion.error('Error interno del servidor')
        return render_template('main/agregar_registro.html', 
                             registro_productos=[], 
                             total_items=0, 
                             total_general=0,
                             vendedores=[],
                             establecimientos=[])

#COMPRA       
@main_bp.route('/compra/guardar', methods=['POST'])
@login_required
def guardar_compra():
    try:
        user_id = session.get('user_id')
        if not user_id:
            Notificacion.error('Error de sesión')
            return redirect(url_for('auth.login'))
        
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')  # Nuevo campo
        vendedor_id = request.form.get('vendedor')
        establecimiento_id = request.form.get('establecimiento')
        
        if vendedor_id and establecimiento_id:
            Notificacion.error('Solo puedes seleccionar vendedor o establecimiento, no ambos')
            return redirect(url_for('main.registro_agregar'))
        
        if not vendedor_id and not establecimiento_id:
            Notificacion.error('Debes seleccionar un vendedor o establecimiento')
            return redirect(url_for('main.registro_agregar'))
        
        if not fecha or not hora:  
            Notificacion.error('La fecha y hora son obligatorias')
            return redirect(url_for('main.registro_agregar'))
        
        result_registro = ServicioRegistroTemporal.listar_productos_del_registro()
        if not result_registro['success'] or not result_registro['productos']:
            Notificacion.error('No hay productos en el registro')
            return redirect(url_for('main.registro_agregar'))
        
        vendedor_id = int(vendedor_id) if vendedor_id else None
        establecimiento_id = int(establecimiento_id) if establecimiento_id else None
        
        fecha_hora_str = f"{fecha} {hora}"
        
        result = ServicioCompra.guardar_compra(
            id_usuario=user_id,
            vendedor_id=vendedor_id,
            establecimiento_id=establecimiento_id,
            fecha_compra=fecha_hora_str, 
            productos_registro=result_registro['productos']
        )
        
        if result['success']:
            ServicioRegistroTemporal.limpiar_registro()
            Notificacion.success(result['message'])
            return redirect(url_for('main.registros'))  
        else:
            Notificacion.error(result['message'])
            return redirect(url_for('main.registro_agregar'))
        
    except Exception as e:
        print(f"Error en guardar_compra: {str(e)}")
        Notificacion.error('Error interno del servidor')
        return redirect(url_for('main.registro_agregar'))       
    
#DETALLE    
@main_bp.route('/detalle/producto/agregar', methods=['GET', 'POST'])
@login_required
def detalle_producto_agregar():
    try:
        user_id = session.get('user_id')
        if not user_id:
            Notificacion.error('Error de sesión')
            return redirect(url_for('auth.login'))
        
        if request.method == 'POST':
            producto_id = request.form.get('producto')
            precio = request.form.get('precio')
            cantidad = request.form.get('cantidad')
            descuento = request.form.get('descuento') or 0
            fecha_vencimiento = request.form.get('fecha_vencimiento')
            
            if not producto_id or not precio or not cantidad or not fecha_vencimiento:        
                Notificacion.error('Todos los campos son obligatorios')
                return redirect(url_for('main.detalle_producto_agregar'))
            
            try:
                producto_id = int(producto_id)
                print(f"[DEBUG] Producto ID convertido a int: {producto_id}")
            except (ValueError, TypeError):
                print(f"[ERROR] Producto ID no válido: {producto_id}")
                Notificacion.error('Producto seleccionado no válido')
                return redirect(url_for('main.detalle_producto_agregar'))
            
            result = ServicioRegistroTemporal.agregar_producto_al_registro(
                producto_id=producto_id,
                precio=precio,
                cantidad=cantidad,
                descuento=descuento,
                fecha_vencimiento=fecha_vencimiento
            )
            
            if result['success']:
                Notificacion.success(result['message'])
                return redirect(url_for('main.registro_agregar'))
            else:
                Notificacion.error(result['message'])
                return redirect(url_for('main.detalle_producto_agregar'))
        
        result_productos = ServicioProducto.listar_productos()
        
        if not result_productos['success']:
            Notificacion.error('Error al cargar los productos')
            productos = []
        else:
            productos = result_productos['productos']
            print(f"[DEBUG] Productos cargados: {len(productos)}")
            for i, p in enumerate(productos[:3]): 
                print(f"[DEBUG] Producto {i+1}: ID={p.get('id', 'N/A')}, Nombre={p.get('nombreProducto', 'N/A')}")
        
        result_registro = ServicioRegistroTemporal.listar_productos_del_registro()
        registro_productos = result_registro['productos'] if result_registro['success'] else []
        
        return render_template(
            'main/gestion_producto_detalle.html',
            modo='agregar',
            productos=productos,
            registro_productos=registro_productos,
            total_items=result_registro.get('total_items', 0),
            total_general=result_registro.get('total_general', 0)
        )
        
    except Exception as e:
        print(f"[ERROR] Error en detalle_producto_agregar: {str(e)}")
        import traceback
        traceback.print_exc()
        Notificacion.error('Error interno del servidor')
        return render_template('main/gestion_producto_detalle.html', 
                             modo='agregar', 
                             productos=[], 
                             registro_productos=[])

@main_bp.route('/detalle/producto/editar/<int:id_temp>', methods=['GET', 'POST'])
@login_required
def detalle_producto_editar(id_temp):
    try:
        user_id = session.get('user_id')
        if not user_id:
            Notificacion.error('Error de sesión')
            return redirect(url_for('auth.login'))
        
        if request.method == 'POST':
            precio = request.form.get('precio')
            cantidad = request.form.get('cantidad')
            descuento = request.form.get('descuento') or 0
            fecha_vencimiento = request.form.get('fecha_vencimiento')
            
            if not all([precio, cantidad, fecha_vencimiento]):
                Notificacion.error('Todos los campos son obligatorios')
                return redirect(url_for('main.detalle_producto_editar', id_temp=id_temp))
            
            result = ServicioRegistroTemporal.editar_producto_del_registro(
                id_temp=id_temp,
                precio=precio,
                cantidad=cantidad,
                descuento=descuento,
                fecha_vencimiento=fecha_vencimiento
            )
            
            if result['success']:
                Notificacion.success(result['message'])
                return redirect(url_for('main.registro_agregar'))
            else:
                Notificacion.error(result['message'])
                return redirect(url_for('main.detalle_producto_editar', id_temp=id_temp))
        
        result_item = ServicioRegistroTemporal.obtener_producto_del_registro(id_temp)
        
        if not result_item['success']:
            Notificacion.error('Producto no encontrado en el registro')
            return redirect(url_for('main.detalle_producto_agregar'))
        
        item = result_item['item']
        
        result_productos = ServicioProducto.listar_productos()
        productos = result_productos['productos'] if result_productos['success'] else []
        
        result_registro = ServicioRegistroTemporal.listar_productos_del_registro()
        registro_productos = result_registro['productos'] if result_registro['success'] else []
        
        return render_template(
            'main/gestion_producto_detalle.html',
            modo='editar',
            item=item,
            productos=productos,
            registro_productos=registro_productos,
            total_items=result_registro.get('total_items', 0),
            total_general=result_registro.get('total_general', 0)
        )
        
    except Exception as e:
        print(f"Error en detalle_producto_editar: {str(e)}")
        Notificacion.error('Error interno del servidor')
        return redirect(url_for('main.detalle_producto_agregar'))
    
@main_bp.route('/detalle/producto/eliminar/<int:id_temp>', methods=['POST'])
@login_required
def detalle_producto_eliminar(id_temp):
    try:
        result = ServicioRegistroTemporal.eliminar_producto_del_registro(id_temp)
        
        if result['success']:
            Notificacion.success(result['message'])
        else:
            Notificacion.error(result['message'])
        
        return redirect(url_for('main.registro_agregar'))
        
    except Exception as e:
        print(f"Error en detalle_producto_eliminar: {str(e)}")
        Notificacion.error('Error interno del servidor')
        return redirect(url_for('main.detalle_producto_agregar')) 
    
@main_bp.route('/detalle/registro/limpiar', methods=['POST'])
@login_required
def detalle_registro_limpiar():
    try:
        result = ServicioRegistroTemporal.limpiar_registro()
        
        if result['success']:
            Notificacion.success(result['message'])
        else:
            Notificacion.error(result['message'])
        
        return redirect(url_for('main.registro_agregar'))
        
    except Exception as e:
        print(f"Error en detalle_registro_limpiar: {str(e)}")
        Notificacion.error('Error interno del servidor')
        return redirect(url_for('main.detalle_producto_agregar')) 
        
#ESTABLECIMIENTO
@main_bp.route('/establecimiento')
@login_required
def establecimiento():
    try:
        user_id = session.get('user_id')
        if not user_id:
            Notificacion.error('Error de sesión')
            return redirect(url_for('auth.login'))
        
        result = ServicioEstablecimiento.listar_establecimientos_usuario(user_id)
        
        if not result['success']:
            Notificacion.error('Error al cargar los establecimientos')
            establecimientos = []
        else:
            establecimientos = result['establecimientos']
        
        return render_template('main/establecimiento.html', establecimientos=establecimientos)
        
    except Exception as e:
        Notificacion.error('Error interno del servidor')
        return render_template('main/establecimiento.html', establecimientos=[])

@main_bp.route('/establecimiento/agregar', methods=['GET', 'POST'])
@login_required
def agregar_establecimiento():
    if request.method == 'POST':
        try:
            user_id = session.get('user_id')
            if not user_id:
                Notificacion.error('Error de sesión')
                return redirect(url_for('auth.login'))
            
            nombre = request.form.get('nombre')
            direccion = request.form.get('direccion')
            hora_apertura = request.form.get('hora_apertura')
            hora_cierre = request.form.get('hora_cierre')
            
            if not all([nombre, direccion, hora_apertura, hora_cierre]):
                Notificacion.error('Todos los campos son obligatorios')
                return render_template('main/gestion_establecimiento.html', modo='agregar')
            
            result = ServicioEstablecimiento.crear_establecimiento(
                nombre, direccion, hora_apertura, hora_cierre, user_id
            )
            
            if result['success']:
                Notificacion.success(result['message'])
                return redirect(url_for('main.establecimiento'))
            else:
                Notificacion.error(result['message'])
                return render_template('main/gestion_establecimiento.html', modo='agregar')
                
        except Exception as e:
            Notificacion.error('Error interno del servidor')
            return render_template('main/gestion_establecimiento.html', modo='agregar')
    
    return render_template('main/gestion_establecimiento.html', modo='agregar')

@main_bp.route('/establecimiento/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_establecimiento(id):
    try:
        user_id = session.get('user_id')
        if not user_id:
            Notificacion.error('Error de sesión')
            return redirect(url_for('auth.login'))
        
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            direccion = request.form.get('direccion')
            hora_apertura = request.form.get('hora_apertura')
            hora_cierre = request.form.get('hora_cierre')
            
            if not all([nombre, direccion, hora_apertura, hora_cierre]):
                Notificacion.error('Todos los campos son obligatorios')
                result = ServicioEstablecimiento.obtener_establecimiento(id, user_id)
                establecimiento = result['establecimiento'] if result['success'] else None
                return render_template('main/gestion_establecimiento.html', 
                                     modo='editar', est=establecimiento)
            
            result = ServicioEstablecimiento.actualizar_establecimiento(
                id, nombre, direccion, hora_apertura, hora_cierre, user_id
            )
            
            if result['success']:
                Notificacion.success(result['message'])
                return redirect(url_for('main.establecimiento'))
            else:
                Notificacion.error(result['message'])
                result_est = ServicioEstablecimiento.obtener_establecimiento(id, user_id)
                establecimiento = result_est['establecimiento'] if result_est['success'] else None
                return render_template('main/gestion_establecimiento.html', 
                                     modo='editar', est=establecimiento)
        
        result = ServicioEstablecimiento.obtener_establecimiento(id, user_id)
        
        if not result['success']:
            Notificacion.error('Establecimiento no encontrado o no tienes permisos para editarlo')
            return redirect(url_for('main.establecimiento'))
        
        establecimiento = result['establecimiento']
        return render_template('main/gestion_establecimiento.html', 
                             modo='editar', est=establecimiento)
        
    except Exception as e:
        Notificacion.error('Error interno del servidor')
        return redirect(url_for('main.establecimiento'))