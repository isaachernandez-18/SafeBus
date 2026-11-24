"""Datos de ejemplo de los perfiles. Más adelante se pueden reemplazar por una base de datos."""

PERFILES = {
    "padre": {
        "nombre": "María García",
        "email": "maria.garcia@email.com",
        "telefono": "+507 6000-0000",
        "direccion": "La Chorrera, Panamá",
    },
    "hijo": {
        "nombre": "Sebastián García",
        "colegio": "La Salle School",
        "grado": "6th Grade",
        "ruta": "Chorrera-West",
        "punto_recogida": "Home",
        "notas": "",
    },
}

# (clave del dato, etiqueta que ve el usuario, texto de ayuda, ¿varias líneas?)
CAMPOS = {
    "padre": [
        ("nombre", "Full name", "e.g. María García", False),
        ("email", "Email", "name@email.com", False),
        ("telefono", "Phone", "+507 6000-0000", False),
        ("direccion", "Home address", "Street, district", False),
    ],
    "hijo": [
        ("nombre", "Full name", "Student's full name", False),
        ("colegio", "School", "School name", False),
        ("grado", "Grade", "e.g. 6th Grade", False),
        ("ruta", "Bus route", "e.g. Chorrera-West", False),
        ("punto_recogida", "Pickup point", "e.g. Home", False),
        ("notas", "Notes for the driver", "", True),
    ],
}


def iniciales(nombre):
    """'María García' -> 'MG'"""
    partes = nombre.split()
    if not partes:
        return "?"
    if len(partes) == 1:
        return partes[0][:2].upper()
    return (partes[0][0] + partes[-1][0]).upper()