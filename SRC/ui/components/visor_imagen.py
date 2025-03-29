import numpy as np
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QPinchGesture
from PyQt6.QtGui import QPixmap, QImage, QWheelEvent
from PyQt6.QtCore import Qt, QEvent
from logic import libreriaManipulacion as lm
from ui import styles as st

class VisorImagen(QWidget):
    
    def __init__(self):
        super().__init__()
        self.imagen = None
        self.imagen_base = None
        self.imagen_original = None
        self.zoom_factor = 1.0
        self.initUI()
        
        # Habilitar la aceptación de eventos táctiles y de gestos
        self.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.grabGesture(Qt.GestureType.PinchGesture)
    
    def event(self, event):
        # Captura el gesto de pellizco
        if event.type() == QEvent.Type.Gesture:
            return self.gestureEvent(event)
        return super().event(event)

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
            self.zoom_factor = 1.0 
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
            # scaled_pixmap = pixmap.scaled(label_size * self.zoom_factor, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
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

    def ajustarContrastePositivo(self, valor):
        """ Ajusta el contraste usando el valor del slider """
        if self.imagen_base is not None:
            self.imagen = lm.ajusteContraste(self.imagen_base, valor, 1)
            self.mostrarImagen()
            
    def ajustarContrasteNegativo(self, valor):
        """ Ajusta el contraste usando el valor del slider """
        if self.imagen_base is not None:
            self.imagen = lm.ajusteContraste(self.imagen_base, valor, 0)
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

    def reiniciarImagen(self):
        """ Restaura la imagen original """
        if self.imagen_original is not None:
            self.imagen = self.imagen_original.copy()
            self.mostrarImagen()

    def aplicarCapaImagen(self, imagen_capa):
        """ Aplica la capa de imagen a la imagen base """
        if self.imagen_base is not None:
            self.imagen = lm.capaImagen(self.imagen_base, imagen_capa)
            self.mostrarImagen()


    def aplicarQuitarCanal(self, canal):
        """ Aplica o quita el canal de la imagen base """
        if self.imagen_base is not None:
            self.imagen = lm.quitarCanal(self.imagen_base, canal)
            self.mostrarImagen()
    
    def aplicarZoom(self, factor, cursor_x=None, cursor_y=None):
        """Aplica zoom a la imagen basada en un factor y opcionalmente en la posición del cursor."""
        if self.imagen_base is not None:
            h, w = self.imagen_base.shape[:2]
            
            if cursor_x is None or cursor_y is None:
                cursor_x, cursor_y = w // 2, h // 2  # Zoom centrado si no se proporciona posición
            
            self.zoom_factor *= factor
            self.zoom_factor = max(0.1, min(self.zoom_factor, 5.0))  # Limitar el zoom
            
            self.imagen = lm.aplicar_zoom(self.imagen_base, self.zoom_factor, cursor_x, cursor_y)
            self.mostrarImagen()

    def setZoomCombo(self, zoom_text, cursor_x=None, cursor_y=None):
        """
        Establece el zoom de la imagen de forma absoluta basado en una opción predefinida.
        zoom_text: cadena con el valor del zoom, por ejemplo "100%" (donde 100% es tamaño normal).
        """
        # Extraer el valor numérico y convertir a factor (por ejemplo, "120%" -> 1.2)
        try:
            zoom_value = int(zoom_text.replace("%", ""))
        except ValueError:
            zoom_value = 100  # valor por defecto si falla la conversión
        
        factor = zoom_value / 100.0  # 1.0 es tamaño normal

        if self.imagen_base is not None:
            h, w = self.imagen_base.shape[:2]
            # Si no se provee la posición, se toma el centro de la imagen
            if cursor_x is None or cursor_y is None:
                cursor_x, cursor_y = w // 2, h // 2
            self.zoom_factor = factor
            self.imagen = lm.aplicar_zoom(self.imagen_base, self.zoom_factor, cursor_x, cursor_y)
            self.mostrarImagen()

    def wheelEvent(self, event: QWheelEvent):
        """Detecta el desplazamiento de la rueda del mouse o el touchpad y aplica zoom."""
        delta = event.angleDelta().y()
        if delta == 0:
            delta = event.pixelDelta().y()
        factor = 1.1 if delta > 0 else 0.9

        # La posición del evento está en coordenadas del widget (self)
        # Convertirla a coordenadas relativas al QLabel
        cursor_global = event.globalPosition().toPoint()
        cursor_local = self.labelImagen.mapFromGlobal(cursor_global)

        # Calcular la posición del cursor sobre la imagen mostrada:
        label_size = self.labelImagen.size()
        if self.imagen_base is None:
            return
        img_h, img_w = self.imagen_base.shape[:2]
        scale = min(label_size.width() / img_w, label_size.height() / img_h)
        offset_x = (label_size.width() - img_w * scale) / 2
        offset_y = (label_size.height() - img_h * scale) / 2
        image_x = (cursor_local.x() - offset_x) / scale
        image_y = (cursor_local.y() - offset_y) / scale

        self.aplicarZoom(factor, int(image_x), int(image_y))

    def gestureEvent(self, event):
        pinch = event.gesture(Qt.GestureType.PinchGesture)
        if pinch:
            scaleFactor = pinch.scaleFactor()
            # Mapear el centro del gesto al QLabel
            center_global = pinch.centerPoint().toPoint()
            center_local = self.labelImagen.mapFromGlobal(center_global)
            label_size = self.labelImagen.size()
            if self.imagen_base is None:
                return True
            img_h, img_w = self.imagen_base.shape[:2]
            scale = min(label_size.width() / img_w, label_size.height() / img_h)
            offset_x = (label_size.width() - img_w * scale) / 2
            offset_y = (label_size.height() - img_h * scale) / 2
            image_x = (center_local.x() - offset_x) / scale
            image_y = (center_local.y() - offset_y) / scale
            self.aplicarZoom(scaleFactor, int(image_x), int(image_y))
        return True

    def aplicarFiltroZonas(self, umbral, modo, color):
        """
        Aplica el filtro de zonas claras u oscuras a la imagen base.
        
        Parámetros:
        - umbral (float): Umbral entre 0 y 1.
        - modo (str): 'claras' o 'oscuras'.
        - color (list): Color en formato RGB normalizado.
        """
        if self.imagen_base is not None:
            # Llama a la función de la librería de manipulación
            self.imagen = lm.filtrar_zonas_claras_oscuras(self.imagen_base, umbral, modo, color)
            self.mostrarImagen()

    def mostrarHistograma(self):
        if self.imagen is not None:
            lm.histograma_imagen(self.imagen)


