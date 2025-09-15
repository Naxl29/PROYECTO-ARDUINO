from functools import wraps
from flask import session, redirect, url_for, flash
from config.roles_config import ROLES, LED_NAMES

def require_role(allowed_roles):
    """
    Decorador para verificar permisos de rol
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'id_usuario' not in session:
                return redirect(url_for('login'))
            
            user_role = session.get('rol', 'USER')
            if user_role not in allowed_roles:
                flash('No tienes permisos para acceder a esta función', 'error')
                return redirect(url_for('dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def can_control_led(led_id, user_role):
    """
    Verifica si un usuario puede controlar un LED específico según su rol
    """
    if user_role not in ROLES:
        return False
    
    allowed_leds = ROLES[user_role]['permissions']['accessible_leds']
    return led_id in allowed_leds

def get_role_info(user_role):
    """
    Obtiene la información completa del rol del usuario
    """
    return ROLES.get(user_role, ROLES['USER'])

def get_led_name(led_id):
    """
    Obtiene el nombre descriptivo de un LED
    """
    return LED_NAMES.get(led_id, f'LED {led_id}')

def check_session():
    """
    Verifica si hay una sesión activa
    """
    return 'id_usuario' in session

def get_user_info():
    """
    Obtiene la información básica del usuario de la sesión
    """
    if not check_session():
        return None
    
    return {
        'id_usuario': session.get('id_usuario'),
        'usuario': session.get('usuario'),
        'rol': session.get('rol', 'USER')
    }
