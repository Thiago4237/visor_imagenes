import os
from PyQt6.QtWidgets import QToolBar, QLabel, QWidget, QSizePolicy, QFileDialog
from PyQt6.QtGui import QIcon, QPixmap, QAction
from PyQt6.QtCore import QSize
import config.config as cfg

class BarraHerramientasSuperior(QToolBar):
    def __init__(self, parent):
        super().__init__("Barra principal")
        self.setIconSize(QSize(32, 32))        
        
        # Agregar logo a la izquierda
        logo_path = cfg.LOGOS["logo"]
        logo_label = QLabel()
        logo_pixmap = QPixmap(logo_path)
        
        # # Verificar que la imagen se cargó correctamente
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap)
            logo_label.setScaledContents(True)  # Permitir que QLabel escale bien la imagen
        
        logo_label.setFixedSize(34, 34)
        self.addWidget(logo_label)
        
        # Añadir espacio flexible para empujar los siguientes botones a la derecha
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.addWidget(spacer)
        
        # Botones de acción
        self.initActionsTop(parent)
    
    def initActionsTop(self, parent):
        cargar_icon_path = cfg.ICONOS["cargar"]
        cargar_action = QAction(QIcon(cargar_icon_path), "Cargar", parent)
        cargar_action.setCheckable(True) 
        cargar_action.triggered.connect(lambda: self.cargarImagen(parent))
        cargar_action.setShortcut(cfg.ATAJOS["cargar"])
        self.addAction(cargar_action)
        
        actualizar_icon_path = cfg.ICONOS["actualizar"]
        actualizar_action = QAction(QIcon(actualizar_icon_path), "Actualizar", parent)
        actualizar_action.setCheckable(True) 
        # actualizar_action.triggered.connect(parent.self.mostrarImagen) # Aún no esta
        actualizar_action.setShortcut(cfg.ATAJOS["actualizar"])
        self.addAction(actualizar_action)
        
        guardar_icon_path = cfg.ICONOS["guardar"]
        guardar_action = QAction(QIcon(guardar_icon_path), "Guardar", parent)
        guardar_action.setCheckable(True) 
        guardar_action.triggered.connect(lambda: self.guardarImagen(parent))
        guardar_action.setShortcut(cfg.ATAJOS["guardar"])
        self.addAction(guardar_action)
    
    # Se obtiene la ruta del archivo para luego llamar a visor_imagen.py que es la que carga la imagen
    def cargarImagen(self, parent):
        filePath, _ = QFileDialog.getOpenFileName(parent, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.bmp)")
        
        # Buscar quién fue el emisor (el botón que se presionó)
        sender = self.sender()
        if isinstance(sender, QAction) and sender.isCheckable():
            sender.setChecked(False)  # Desmarca el botón
        
        if filePath:
            parent.visor.cargarImagen(filePath)

    def guardarImagen(self, parent):
        filePath, _ = QFileDialog.getSaveFileName(parent, "Guardar imagen", "", "Imágenes (*.png *.jpg *.bmp)")
        
        # Buscar quién fue el emisor (el botón que se presionó)
        sender = self.sender()
        if isinstance(sender, QAction) and sender.isCheckable():
            sender.setChecked(False)  # Desmarca el botón
        
        if filePath:
            parent.visor.guardarImagen(filePath)
