from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtGui import QIcon 
from PyQt6.QtCore import Qt
from ui.components.barra_superior import BarraSuperior
from ui.components.barra_lateral import BarraLateral
from ui.components.visor_imagen import VisorImagen
from ui import styles as st
import config.config as cfg

class VisorImagenes(QMainWindow):
    """
    Clase principal que representa la ventana del visor de imágenes.
    
    Esta clase hereda de QMainWindow y organiza todos los componentes de la interfaz,
    incluyendo las barras de herramientas, el visor de imágenes y el estilo general
    de la aplicación. Actúa como contenedor principal y coordinador de todos los
    widgets y funcionalidades.
    
    Atributos:
        visor (VisorImagen): Componente central que muestra y manipula las imágenes.
    
    Métodos:
        inicializarUI: Configura la interfaz de usuario con todos sus componentes.
    """
    def __init__(self):
        """
        Inicializa una instancia de la clase VisorImagenes.
        
        Este método configura la ventana principal de la aplicación y crea
        el componente visor de imágenes que será utilizado por las barras
        de herramientas para manipular las imágenes.
        
        Acciones:
            - Llama al constructor de la clase base QMainWindow.
            - Inicializa el visor de imágenes antes que las barras de herramientas.
            - Llama al método inicializarUI para configurar la interfaz.
        """
        super().__init__()
        self.visor = VisorImagen()  # Inicializar visor antes de la barra de herramientas
        self.inicializarUI()

    def inicializarUI(self):
        """
        Configura la interfaz de usuario de la aplicación.
        
        Este método establece las propiedades de la ventana principal y añade
        todos los componentes necesarios para la interfaz, incluyendo las barras
        de herramientas y el visor de imágenes.
        
        Acciones:
            - Configura la ventana principal (tamaño, título, icono).
            - Crea y añade la barra de herramientas superior.
            - Crea y añade la barra lateral derecha.
            - Aplica estilos visuales a la interfaz.
            - Crea un contenedor principal para organizar los elementos.
            - Agrega el visor de imágenes como widget central.
            
        Componentes creados:
            - BarraSuperior: Barra de herramientas con acciones comunes.
            - BarraLateral: Barra lateral para ajustes y controles.
            - QWidget (contenedor): Contenedor principal con estilo aplicado.
            - QVBoxLayout: Layout vertical para organizar elementos.
        """
        self.setWindowState(Qt.WindowState.WindowMaximized)
        self.setWindowTitle("Visor de imágenes")
        self.setMinimumSize(800, 600)
        
        #icono de la ventana
        icon_path = cfg.LOGOS["logo"]
        self.setWindowIcon(QIcon(icon_path))

        # Crear barra de herramientas Superior
        toolbar = BarraSuperior(self)
        self.addToolBar(toolbar)
        
        # Barra lateral derecha
        toolbar_lateral = BarraLateral(self)
        self.addToolBar(Qt.ToolBarArea.RightToolBarArea, toolbar_lateral)
        
        #Estilos de las barras
        self.setStyleSheet(st.TOOLBAR_STYLE)

        # Contenedor principal
        contenedor = QWidget()
        contenedor.setStyleSheet(st.MAIN_CONTAINER_STYLE)
        layout_principal_vertical = QVBoxLayout(contenedor)

        # Agregar visor de imágenes
        layout_principal_vertical.addWidget(self.visor)

        self.setCentralWidget(contenedor)