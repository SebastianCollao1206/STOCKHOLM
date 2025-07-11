from flask import Blueprint, render_template, request, redirect, url_for, session
from app.utils.notificaciones import Notificacion
from app.service.user_service import ServicioUsuario
from app.utils.auth_decorators import guest_only

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
@guest_only
def login():
    return render_template('auth/login.html')

@auth_bp.route('/registro')
@guest_only
def registro():
    return render_template('auth/registro.html')

@auth_bp.route('/login', methods=['POST'])
@guest_only
def login_post():
    correo = request.form.get('email')
    clave = request.form.get('password')
    
    result = ServicioUsuario.autenticar_usuario_por_correo(correo, clave)
    
    if result['success']:
        session['user_id'] = result['user']['idUsuario']
        session['user_name'] = result['user']['usuario']
        session['user_email'] = result['user']['correo']
        Notificacion.success('¡Bienvenido de vuelta!', f"Hola {result['user']['usuario']}")
        return redirect(url_for('main.registros'))  
    else:
        Notificacion.error(result['message'])
        return redirect(url_for('auth.login'))

@auth_bp.route('/registro', methods=['POST'])
@guest_only
def registro_post():
    nombre = request.form.get('name')
    correo = request.form.get('email')
    clave = request.form.get('password')
    
    result = ServicioUsuario.registrar_usuario(nombre, correo, clave)
    
    if result['success']:
        Notificacion.success(result['message'])
        return redirect(url_for('auth.login'))  
    else:
        Notificacion.error(result['message'])
        return redirect(url_for('auth.registro'))
    
@auth_bp.route('/logout')
def logout():
    session.clear()
    Notificacion.success('Has cerrado sesión exitosamente')
    return redirect(url_for('auth.login'))