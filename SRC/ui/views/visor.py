from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtGui import QIcon 
from PyQt6.QtCore import Qt
from ui.components.barra_superior import BarraSuperior
from ui.components.barra_lateral import BarraLateral
from ui.components.visor_imagen import VisorImagen
from ui import styles as st
import config.config as cfg

class VisorImagenes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.visor = VisorImagen()  # Inicializar visor antes de la barra de herramientas
        self.inicializarUI()

    def inicializarUI(self):
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