import numpy as np
import os
from PyQt6.QtWidgets import (QMainWindow, QWidget, QFileDialog, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLineEdit)
from PyQt6.QtGui import QPixmap, QIcon, QPixmap, QImage
from PyQt6.QtCore import Qt
from logic import libreriaManipulacion as lm

class VisorImagenes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.inicializarUI()

    def inicializarUI(self):     
        self.setWindowState(Qt.WindowState.WindowMaximized)   
        self.setWindowTitle("Visor de imágenes")      
        self.setMinimumSize(800, 600) 
        
        # Ruta para el icono de la ventana
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "img", "logo.png"))
        self.setWindowIcon(QIcon(icon_path)) 
        
        # Contenedor principal con layout vertical
        contenedor = QWidget()
        layout_principal_vertical = QVBoxLayout(contenedor)
        
        # Agregar título en la parte superior
        self.titulo = QLabel("Visor de Imágenes")
        self.titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        layout_principal_vertical.addWidget(self.titulo)
        
        # Layout horizontal para la imagen y controles (va debajo del título)
        layout_horizontal = QHBoxLayout()
        layout_principal_vertical.addLayout(layout_horizontal)
        
        # Área de imagen (izquierda)
        layout_imagen = QVBoxLayout()
        self.labelImagen = QLabel("No hay imagen cargada")
        self.labelImagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_imagen.addWidget(self.labelImagen)
        
        # Barra de ruta (debajo de la imagen)
        layout_ruta = QHBoxLayout()
        etiqueta_ruta = QLabel("Ruta de la imagen:")
        self.barraRuta = QLineEdit()
        self.barraRuta.setReadOnly(True)
        layout_ruta.addWidget(etiqueta_ruta)
        layout_ruta.addWidget(self.barraRuta)
        layout_imagen.addLayout(layout_ruta)
        
        # Controles (derecha)
        layout_controles = QVBoxLayout()
        self.btnCargar = QPushButton("Cargar Imagen")
        self.btnCargar.clicked.connect(self.cargarImagen)
        layout_controles.addWidget(self.btnCargar)
        
        self.btnGuardar = QPushButton("Guardar Imagen")
        self.btnGuardar.clicked.connect(self.guardarImagen)
        layout_controles.addWidget(self.btnGuardar)
        
        layout_controles.addStretch()  # Empuja los botones hacia arriba
        
        # Agregar layouts al layout horizontal
        layout_horizontal.addLayout(layout_imagen, 3)
        layout_horizontal.addLayout(layout_controles, 1)
        
        self.setCentralWidget(contenedor)
        self.imagen = None 

    # Obtiene la imagen del disco
    def cargarImagen(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Seleccionar Imagen", "", "Images (*.png *.jpg *.bmp)")
        if filePath:
            self.imagen = lm.cargar_imagen(filePath)
            self.mostrarImagen()
            self.barraRuta.setText(filePath)  # Mostrar la ruta en la barra

    # Convierte y muestra la imagen en la interfaz gráfica
    def mostrarImagen(self):
        if self.imagen is not None:
            # Convertir a uint8 (0-255)
            img = (self.imagen * 255).astype(np.uint8)
            
            # Verificar la forma de la imagen
            if len(img.shape) == 2:  # Imagen en escala de grises
                h, w = img.shape
                # Crear una imagen en escala de grises
                qImg = QImage(img.data, w, h, w, QImage.Format.Format_Grayscale8)
            elif img.shape[2] == 3:  # Imagen RGB
                h, w, c = img.shape
                # Asegurarse de que los datos estén contiguos en memoria
                img = np.ascontiguousarray(img)
                bytesPerLine = 3 * w
                qImg = QImage(img.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)
            elif img.shape[2] == 4:  # Imagen RGBA
                h, w, c = img.shape
                img = np.ascontiguousarray(img)
                bytesPerLine = 4 * w
                qImg = QImage(img.data, w, h, bytesPerLine, QImage.Format.Format_RGBA8888)
            else:
                return  # Formato no soportado
                
            # Crear un pixmap con la imagen
            pixmap = QPixmap.fromImage(qImg)
            
            # Escalar la imagen manteniendo la proporción para que se ajuste al label
            label_size = self.labelImagen.size()
            scaled_pixmap = pixmap.scaled(label_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            
            # Mostrar la imagen escalada
            self.labelImagen.setPixmap(scaled_pixmap)
            self.labelImagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
    # Actualizar automáticamente la imagen cuando se redimension
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Volver a mostrar la imagen cuando se redimensiona la ventana
        if self.imagen is not None:
            self.mostrarImagen()
            
    def guardarImagen(self):
        if self.imagen is not None:
            filePath, _ = QFileDialog.getSaveFileName(self, "Guardar Imagen", "", "Images (*.png *.jpg *.bmp)")
            if filePath:
                lm.guardar_imagen(filePath, self.imagen)
