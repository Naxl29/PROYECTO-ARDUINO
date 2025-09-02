# Configuración de roles y permisos
ROLES = {
    'ADMIN': {
        'name': 'Administrador',
        'permissions': {
            'can_view_all_reports': True,
            'can_control_all_leds': True,
            'can_use_all_button': True,
            'accessible_leds': ['1', '2', '3', '4', '5', '6', '7', '8', 'ALL']
        }
    },
    'USER': {
        'name': 'Usuario Normal',
        'permissions': {
            'can_view_all_reports': False,
            'can_control_all_leds': False,
            'can_use_all_button': False,
            'accessible_leds': ['1', '2', '3', '4', '5', '6', '7', '8']
        }
    },
    'CHILD': {
        'name': 'Usuario Niño',
        'permissions': {
            'can_view_all_reports': False,
            'can_control_all_leds': False,
            'can_use_all_button': False,
            'accessible_leds': ['1', '2', '3', '4']
        }
    }
}

LED_NAMES = {
    '1': 'LUZ SALA',
    '2': 'LUZ COCINA', 
    '3': 'LUZ HABITACIÓN',
    '4': 'LUZ BAÑO',
    '5': 'AIRE ACONDICIONADO',
    '6': 'LAVADORA',
    '7': 'NEVERA',
    '8': 'TELEVISOR',
    'ALL': 'ENCENDER TODOS'
}
