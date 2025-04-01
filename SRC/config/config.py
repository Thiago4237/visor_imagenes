import os

# Obtener la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, "../../Resources")

# Definir rutas a las subcarpetas
LOGOS_DIR = os.path.join(RESOURCES_DIR, "img")
ICONOS_DIR = os.path.join(RESOURCES_DIR, "iconos")

# Función para obtener rutas de archivos
def get_logo_path(filename):
    """Obtiene la ruta completa para un archivo de logo"""
    return os.path.join(LOGOS_DIR, filename)

def get_icon_path(filename):
    """Obtiene la ruta completa para un archivo de icono"""
    return os.path.join(ICONOS_DIR, filename)

# Rutas de logos e iconos
LOGOS = {
    "logo": get_logo_path("logo.png"),
}

ICONOS = {
    "cargar": get_icon_path("cargar.png"),
    "actualizar": get_icon_path("actualizar.png"),
    "guardar": get_icon_path("guardar.png"),
    "ajustesBasicos": get_icon_path("ajustesBasicos2.png"),
    "ajustesDeFiltros": get_icon_path("ajustesFiltros.png"),
    "ajustesAvanzados": get_icon_path("ajustesAvanzados.png"),
    "deshacer": get_icon_path("deshacer.png"),
    "rehacer": get_icon_path("rehacer.png"),
}

# Atajos de teclado
ATAJOS = {
    "cargar": "Ctrl+C",
    "actualizar": "Ctrl+A",
    "guardar": "Ctrl+G",
    "deshacer": "Ctrl+Z",
    "rehacer": "Ctrl+Y",
    "ajustesBasicos": "1",
    "ajustesDeFiltros": "2",
    "ajustesAvanzados": "3",
}