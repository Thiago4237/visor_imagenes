import os
from PyQt6.QtWidgets import QToolBar, QLabel, QWidget, QSizePolicy, QFileDialog, QComboBox
from PyQt6.QtGui import QIcon, QPixmap, QAction
from PyQt6.QtCore import QSize
import config.config as cfg

class BarraSuperior(QToolBar):
    def __init__(self, parent):
        super().__init__("Barra principal")
        self.parent_widget = parent  # Almacenar referencia al parent
        self.setIconSize(QSize(32, 32))        
        
        # Agregar logo a la izquierda
        logo_path = cfg.LOGOS["logo"]
        logo_label = QLabel()
        logo_pixmap = QPixmap(logo_path)
        
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap)
            logo_label.setScaledContents(True)  # Permitir que QLabel escale bien la imagen
        
        # Tamaño del logo
        logo_label.setFixedSize(38, 38)
        self.addWidget(logo_label)
        
        # Añadir espacio flexible para empujar los botones a la derecha
        spacer_left = QWidget()
        spacer_left.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.addWidget(spacer_left)

        # Añadir espacio flexible para empujar los botones a la izquierda
        spacer_right = QWidget()
        spacer_right.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.addWidget(spacer_right)

        # Botones de acción
        self.initActionsTop()
    
    def initActionsTop(self):
        """Inicializa y agrega los botones a la barra de herramientas."""

         # Botón de Cargar
        cargar_action = self.createAction("cargar", "Cargar", self.cargarImagen)
        cargar_action.setShortcut(cfg.ATAJOS["cargar"])
        self.addAction(cargar_action)

        # Botón de Guardar
        guardar_action = self.createAction("guardar", "Guardar", self.guardarImagen)
        guardar_action.setShortcut(cfg.ATAJOS["guardar"])
        self.addAction(guardar_action)

        self.addSeparator()  # Separador entre botones

        # Botón de Actualizar
        actualizar_action = self.createAction("actualizar", "Actualizar", self.actualizarImagen)
        actualizar_action.setShortcut(cfg.ATAJOS["actualizar"])
        self.addAction(actualizar_action)

        # Botón de Deshacer
        deshacer_action = self.createAction("deshacer", "Deshacer", self.deshacerCambios)
        self.addAction(deshacer_action)

        # Botón de Rehacer
        rehacer_action = self.createAction("rehacer", "Rehacer", self.rehacerCambios)
        self.addAction(rehacer_action)

        
    def createAction(self, icono_nombre, texto, callback):
        """
        Crea un botón de acción con su respectivo icono, texto y función asociada.
        """
        icono_path = cfg.ICONOS[icono_nombre]
        action = QAction(QIcon(icono_path), texto, self.parent_widget)
        action.setCheckable(True)
        action.triggered.connect(callback)
        return action

    def cargarImagen(self):
        """Abre un cuadro de diálogo para seleccionar y cargar una imagen."""
        filePath, _ = QFileDialog.getOpenFileName(self.parent_widget, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.bmp)")
        if filePath:
            self.parent_widget.visor.cargarImagen(filePath)
        self.desmarcarBoton()

    def guardarImagen(self):
        """Abre un cuadro de diálogo para guardar la imagen actual."""
        filePath, _ = QFileDialog.getSaveFileName(self.parent_widget, "Guardar imagen", "", "Imágenes (*.png *.jpg *.bmp)")
        if filePath:
            self.parent_widget.visor.guardarImagen(filePath)
        self.desmarcarBoton()

    def actualizarImagen(self):
        """Llama a la función de actualizar imagen en el visor."""
        self.parent_widget.visor.actualizarImagen()
        self.desmarcarBoton()

    def deshacerCambios(self):
        """Llama a la función de deshacer en el visor de imágenes."""
        self.parent_widget.visor.deshacerCambios()
        self.desmarcarBoton()

    def rehacerCambios(self):
        """Llama a la función de rehacer en el visor de imágenes."""
        self.parent_widget.visor.rehacerCambios()
        self.desmarcarBoton()

    def desmarcarBoton(self):
        """Desmarca el botón después de hacer clic."""
        sender = self.sender()
        if isinstance(sender, QAction) and sender.isCheckable():
            sender.setChecked(False)
