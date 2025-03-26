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
            self.imagen = lm.cargar_imagen(filePath)
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
