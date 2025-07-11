from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.auth_decorators import login_required

main_bp = Blueprint('main', __name__)

#REPORTES
@main_bp.route('/reportes')
@login_required
def reportes():
    return render_template('main/reportes.html')

#VENDEDOR
@main_bp.route('/vendedor/agregar')
@login_required
def vendedor_agregar():
    return render_template('main/agregar_vendedor.html')

#PRESENTACION
@main_bp.route('/presentacion/agregar')
@login_required
def presentacion_agregar():
    return render_template('main/agregar_presentacion.html')

#MARCA
@main_bp.route('/marca/agregar')
@login_required
def marca_agregar():
    return render_template('main/agregar_marca.html')

#INVENTARIO
@main_bp.route('/inventario')
@login_required
def inventario():
    return render_template('main/inventario.html')

#PRODUCTOS
@main_bp.route('/productos')
@login_required
def productos():
    return render_template('main/productos.html')

@main_bp.route('/producto/agregar')
@login_required
def producto_agregar():
    return render_template('main/agregar_producto.html')

#REGISTROS
@main_bp.route('/registros')
@login_required
def registros():
    return render_template('main/registros.html')

@main_bp.route('/detalle/registro/<int:id>', methods=['GET', 'POST'])
@login_required
def detalle_registro(id):
    try:              
        return render_template('main/detalle_registro.html')  
    except Exception as e:
        print(f"Error: {str(e)}")
        return render_template('main/detalle_registro.html')
    
@main_bp.route('/registro/agregar')
@login_required
def registro_agregar():
    return render_template('main/agregar_registro.html')
    
#DETALLE    
@main_bp.route('/detalle/producto/agregar', methods=['GET', 'POST'])
@login_required
def detalle_producto_agregar():
    try:
        if request.method == 'POST':
            producto_id = request.form.get('producto')
            vendedor_id = request.form.get('vendedor')
            cantidad = request.form.get('cantidad')
            descuento = request.form.get('descuento') or 0
            fecha_vencimiento = request.form.get('fecha_vencimiento')

            # Aquí iría la lógica para guardar el detalle
            # DetalleService.crear_detalle(producto_id, vendedor_id, cantidad, descuento, fecha_vencimiento)

            # flash('Producto agregado al detalle exitosamente', 'success')
            # return redirect(url_for('main.algun_listado'))
        return render_template(
            'main/gestion_producto_detalle.html',
            modo='agregar'
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        return render_template('main/gestion_producto_detalle.html', modo='agregar')  

@main_bp.route('/detalle/producto/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def detalle_producto_editar(id):
    try:
        # Obtener el detalle actual desde la BD

        if request.method == 'POST':
            producto_id = request.form.get('producto')
            vendedor_id = request.form.get('vendedor')
            cantidad = request.form.get('cantidad')
            descuento = request.form.get('descuento') or 0
            fecha_vencimiento = request.form.get('fecha_vencimiento')

            # Actualizar el detalle
            # DetalleService.actualizar_detalle(id, producto_id, vendedor_id, cantidad, descuento, fecha_vencimiento)

            # flash('Producto del detalle actualizado exitosamente', 'success')
            # return redirect(url_for('main.algun_listado'))
        return render_template(
            'main/gestion_producto_detalle.html',
            modo='editar'
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        return redirect(url_for('main.detalle_producto_agregar')) 


#ESTABLECIMIENTO
@main_bp.route('/establecimiento/agregar', methods=['GET', 'POST'])
@login_required
def agregar_establecimiento():
    if request.method == 'POST':
        try:
            nombre = request.form.get('nombre')
            direccion = request.form.get('direccion')
            hora_apertura = request.form.get('hora_apertura')
            hora_cierre = request.form.get('hora_cierre')
            # Llamar al servicio para guardar
            # EstablecimientoService.crear_establecimiento(nombre, direccion, hora_apertura, hora_cierre)
            
            # flash('Establecimiento agregado exitosamente', 'success')
            # return redirect(url_for('main.establecimiento'))
        except Exception as e:
            print(f"Error: {str(e)}")
    return render_template('main/gestion_establecimiento.html', modo='agregar')

@main_bp.route('/establecimiento/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_establecimiento(id):
    try:    
        if request.method == 'POST':
            nombre = request.form.get('nombre')
            direccion = request.form.get('direccion')
            hora_apertura = request.form.get('hora_apertura')
            hora_cierre = request.form.get('hora_cierre')
            # Llamar al servicio para actualizar
            # EstablecimientoService.actualizar_establecimiento(id, nombre, direccion, hora_apertura, hora_cierre)
            
            # flash('Establecimiento actualizado exitosamente', 'success')
            # return redirect(url_for('main.establecimiento'))
            
        return render_template('main/gestion_establecimiento.html', modo='editar', est=establecimiento)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return render_template('main/gestion_establecimiento.html', modo='editar', est=establecimiento)


@main_bp.route('/establecimiento')
@login_required
def establecimiento():
    return render_template('main/establecimiento.html')