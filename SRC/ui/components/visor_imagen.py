import numpy as np
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QWidget
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
from logic import libreriaManipulacion as lm
from ui import styles as st

class VisorImagen(QWidget):
    def __init__(self):
        super().__init__()
        self.imagen = None
        self.imagen_base = None
        self.imagen_original = None
        self.initUI()
    
    def initUI(self):
        layout_principal = QVBoxLayout(self)
        
        # Área de imagen
        self.labelImagen = QLabel("No hay imagen cargada")
        self.labelImagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(self.labelImagen)
        
        # Barra de ruta
        layout_ruta = QHBoxLayout()
        etiqueta_ruta = QLabel("Ruta de la imagen:")
        self.barraRuta = QLineEdit()
        self.barraRuta.setReadOnly(True)
        
        etiqueta_ruta.setStyleSheet(st.LABEL_STYLE)
        self.barraRuta.setStyleSheet(st.TEXTFIELD_STYLE)
        
        layout_ruta.addWidget(etiqueta_ruta)
        layout_ruta.addWidget(self.barraRuta)
        layout_principal.addLayout(layout_ruta)
    
    def cargarImagen(self, filePath):
        if filePath:

            self.imagen_original = lm.cargar_imagen(filePath)  # Guardar original
            self.imagen_base = self.imagen_original.copy()  # Base para modificaciones
            self.imagen = self.imagen_original.copy()  # Imagen visualizada

            self.mostrarImagen()
            self.barraRuta.setText(filePath)
    
    def mostrarImagen(self):
        if self.imagen is not None:
            img = (self.imagen * 255).astype(np.uint8)
            
            if len(img.shape) == 2:
                h, w = img.shape
                qImg = QImage(img.data, w, h, w, QImage.Format.Format_Grayscale8)
            elif img.shape[2] == 3:
                h, w, c = img.shape
                img = np.ascontiguousarray(img)
                bytesPerLine = 3 * w
                qImg = QImage(img.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)
            elif img.shape[2] == 4:
                h, w, c = img.shape
                img = np.ascontiguousarray(img)
                bytesPerLine = 4 * w
                qImg = QImage(img.data, w, h, bytesPerLine, QImage.Format.Format_RGBA8888)
            else:
                return
            
            pixmap = QPixmap.fromImage(qImg)
            label_size = self.labelImagen.size()
            scaled_pixmap = pixmap.scaled(label_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.labelImagen.setPixmap(scaled_pixmap)
            self.labelImagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    def guardarImagen(self, filePath):
        if self.imagen is not None and filePath:
            lm.guardar_imagen(filePath, self.imagen)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.imagen is not None:
            self.mostrarImagen()

    def invertirColoresImagen(self):
        """
        Invierte los colores de la imagen actual.
        haciendo llamado a la librería de manipulación.
        """
        if self.imagen is not None:
            self.imagen = lm.invertirColoresImagen(self.imagen)
            self.imagen_base = self.imagen.copy() # Actualizar base modificada
            self.mostrarImagen()

    def aplicarAjusteBrillo(self, valor):
        if self.imagen_base is not None:
            self.imagen = lm.ajusteBrillo(self.imagen_base, valor)
            self.mostrarImagen()

    def ajustarContraste(self, valor):
        """ Ajusta el contraste usando el valor del slider """
        if self.imagen_base is not None:
            tipo = 0 if valor < 1 else 1
            contraste = valor if valor < 1 else valor - 1 
            if contraste > 0:
                self.imagen = lm.ajusteContraste(self.imagen_base, contraste, tipo)
                self.mostrarImagen()

    def binarizarImagen(self):
        """ Binariza la imagen actual """
        if self.imagen_base is not None:
            self.imagen = lm.binarizar_imagen(self.imagen_base)
            self.mostrarImagen()

    def aplicarRotacion(self, angulo):
        """ Aplica la rotación a la imagen y actualiza la vista. """
        if self.imagen_base is not None:
            self.imagen = lm.rotar_imagen(self.imagen_base, angulo)
            self.mostrarImagen()



