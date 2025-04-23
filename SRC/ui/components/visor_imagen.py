import numpy as np
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QWidget
from PyQt6.QtGui import QPixmap, QImage, QWheelEvent
from PyQt6.QtCore import Qt, QEvent
from logic import libreriaManipulacion as lm
from ui import styles as st

class VisorImagen(QWidget):
    """
    Clase que maneja la visualización y manipulación de imágenes en la interfaz gráfica.
    Permite cargar imágenes, aplicar modificaciones y gestionar el historial de cambios.
    """
    
    # --------------------------------------------------
    # configuraciones de la interfaz de usuario
    # --------------------------------------------------
    
    def __init__(self):
        """
        Inicializa una instancia de la clase.
        Atributos:
            imagen (None): Variable para almacenar la imagen actual.
            imagen_base (None): Variable para almacenar la imagen base.
            imagen_original (None): Variable para almacenar la imagen original.
            historial (list): Pila utilizada para deshacer cambios realizados en la imagen.
            redo_stack (list): Pila utilizada para rehacer cambios deshechos.
            zoom_factor (float): Factor de zoom inicializado en 1.0.
        Acciones:
            - Llama al constructor de la clase base.
            - Inicializa los atributos de la clase.
            - Configura la interfaz de usuario llamando a `initUI`.
            - Habilita la aceptación de eventos táctiles y de gestos, incluyendo el gesto de pellizco.
        """
        super().__init__()
        self.imagen = None
        self.imagen_base = None
        self.imagen_original = None
        self.historial = []  # Pila para deshacer cambios
        self.redo_stack = []  # Pila para rehacer cambios
        self.zoom_factor = 1.0
        self.imagen_secundaria = None  # Para almacenar la imagen secundaria
        self.ruta_imagen_secundaria = ""  # Para guardar la ruta de la imagen secundaria
        self.initUI()
        
        # Habilitar la aceptación de eventos táctiles y de gestos
        self.setAttribute(Qt.WidgetAttribute.WA_AcceptTouchEvents, True)
        self.grabGesture(Qt.GestureType.PinchGesture)
    
    def initUI(self):
        """
        Inicializa la interfaz de usuario del visor de imágenes.
        Este método configura el diseño principal y los elementos de la interfaz gráfica,
        incluyendo un área para mostrar imágenes, una etiqueta inicial, y una barra de texto
        de solo lectura para mostrar la ruta de la imagen cargada.
        Componentes:
        - QLabel para mostrar la imagen o un mensaje predeterminado si no hay imagen cargada.
        - QVBoxLayout como diseño principal para organizar los elementos verticalmente.
        - QHBoxLayout para organizar horizontalmente la etiqueta y la barra de texto de la ruta.
        - QLabel para mostrar el texto "Ruta de la imagen:".
        - QLineEdit de solo lectura para mostrar la ruta de la imagen cargada.
        Estilos:
        - Se aplican estilos personalizados a la etiqueta de la ruta y a la barra de texto
          utilizando las constantes `LABEL_STYLE` y `TEXTFIELD_STYLE` definidas en el módulo `st`.
        """
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
        
        # Estilos
        etiqueta_ruta.setStyleSheet(st.LABEL_STYLE)
        self.labelImagen.setStyleSheet(st.LABEL_IMAGE)
        self.barraRuta.setStyleSheet(st.TEXTFIELD_STYLE)
        
        layout_ruta.addWidget(etiqueta_ruta)
        layout_ruta.addWidget(self.barraRuta)
        layout_principal.addLayout(layout_ruta)
    
    # --------------------------------------------------
    # eventos
    # --------------------------------------------------
    
    def event(self, event):
        """
        Maneja los eventos de la clase, incluyendo gestos y otros tipos de eventos.
        Args:
            event (QEvent): El evento que se va a procesar. Puede ser de diferentes tipos, 
            incluyendo gestos.
        Returns:
            bool: Devuelve True si el evento fue procesado correctamente, 
            de lo contrario, delega el manejo del evento a la clase base.
        """
        
        # Captura el gesto de pellizco
        if event.type() == QEvent.Type.Gesture:
            return self.gestureEvent(event)
        return super().event(event)

    def resizeEvent(self, event):
        """
        Método que se ejecuta cuando el componente cambia de tamaño.
        Este método sobrescribe el evento de redimensionamiento de la clase base.
        Si hay una imagen cargada en el componente, se llama al método `mostrarImagen`
        para ajustar la visualización de la imagen al nuevo tamaño del componente.
        Args:
            event (QResizeEvent): Evento de redimensionamiento que contiene información
            sobre el nuevo tamaño del componente.
        """
        super().resizeEvent(event)
        if self.imagen is not None:
            self.mostrarImagen()

    def wheelEvent(self, event: QWheelEvent):
        """
        Maneja el evento de la rueda del ratón para aplicar zoom en una imagen.
        Este método se activa cuando el usuario utiliza la rueda del ratón
        mientras el cursor está sobre el widget. Calcula el factor de zoom
        basado en la dirección del desplazamiento de la rueda y determina
        la posición del cursor en la imagen mostrada para realizar el zoom
        centrado en esa posición.
        Args:
            event (QWheelEvent): El evento de la rueda del ratón que contiene
            información sobre el desplazamiento y la posición del cursor.
        Notas:
            - Si no hay una imagen cargada (`self.imagen` es None), el método
              retorna sin realizar ninguna acción.
            - La posición del cursor se convierte de coordenadas del widget
              a coordenadas relativas a la imagen mostrada.
            - Llama al método `aplicarZoom` con el factor de zoom calculado
              y las coordenadas de la posición del cursor sobre la imagen.
        """
        
        # Verificar si tenemos una imagen cargada
        if self.imagen is None:
            return
            
        # Obtener el delta de la rueda del ratón
        delta = event.angleDelta().y()
        if delta == 0:
            delta = event.pixelDelta().y()
        
        # Calcular el factor de zoom - hacerlo más agresivo (25% en lugar de 10%)
        factor = 1.25 if delta > 0 else 0.8
        
        # Convertir coordenadas del cursor para centrar el zoom correctamente
        cursor_global = event.globalPosition().toPoint()
        cursor_local = self.labelImagen.mapFromGlobal(cursor_global)

        # Calcular la posición del cursor sobre la imagen mostrada
        label_size = self.labelImagen.size()
        img_h, img_w = self.imagen.shape[:2]
        scale = min(label_size.width() / img_w, label_size.height() / img_h)
        offset_x = (label_size.width() - img_w * scale) / 2
        offset_y = (label_size.height() - img_h * scale) / 2
        
        # Convertir coordenadas del cursor relativas a la imagen
        image_x = (cursor_local.x() - offset_x) / scale
        image_y = (cursor_local.y() - offset_y) / scale

        # Aplicar el zoom con el factor calculado
        self.aplicarZoom(factor, int(image_x), int(image_y))

    def gestureEvent(self, event):
        """
        Maneja el evento de gesto, específicamente el gesto de pellizco (pinch gesture),
        para aplicar un zoom en una imagen mostrada en un QLabel.
        Args:
            event (QGestureEvent): El evento de gesto que contiene información sobre
            los gestos detectados.
        Returns:
            bool: Devuelve True para indicar que el evento ha sido manejado.
        Detalles:
            - Detecta si el gesto es un PinchGesture.
            - Calcula el factor de escala del gesto.
            - Mapea el centro del gesto desde coordenadas globales a locales dentro del QLabel.
            - Calcula las coordenadas de la imagen en función del gesto y el escalado actual.
            - Llama al método `aplicarZoom` con el factor de escala y las coordenadas calculadas.
        """
        
        pinch = event.gesture(Qt.GestureType.PinchGesture)
        if pinch and self.imagen is not None:
            # Amplificar el factor de escala para hacerlo más sensible
            scaleFactor = pinch.scaleFactor()
            # Si el factor es muy cercano a 1, podemos amplificarlo para hacerlo más efectivo
            if 0.9 < scaleFactor < 1.1:
                # Amplificamos el factor para hacerlo más sensible
                if scaleFactor > 1:
                    scaleFactor = 1 + (scaleFactor - 1) * 2.5  # Amplificar el zoom in
                else:
                    scaleFactor = 1 - (1 - scaleFactor) * 2.5  # Amplificar el zoom out
            
            # Mapear el centro del gesto al QLabel
            center_global = pinch.centerPoint().toPoint()
            center_local = self.labelImagen.mapFromGlobal(center_global)
            label_size = self.labelImagen.size()
            img_h, img_w = self.imagen.shape[:2]
            scale = min(label_size.width() / img_w, label_size.height() / img_h)
            offset_x = (label_size.width() - img_w * scale) / 2
            offset_y = (label_size.height() - img_h * scale) / 2
            image_x = (center_local.x() - offset_x) / scale
            image_y = (center_local.y() - offset_y) / scale            
            
            self.aplicarZoom(scaleFactor, int(image_x), int(image_y))
        return True

    # --------------------------------------------------
    # manejo imagens
    # --------------------------------------------------
    
    def cargarImagen(self, filePath):
        """
        Carga una imagen desde la ruta especificada y la prepara para su visualización y edición.

        Parámetros:
            filePath (str): Ruta del archivo de la imagen a cargar.

        Comportamiento:
        - Carga la imagen desde la ruta proporcionada utilizando `lm.cargar_imagen(filePath)`.
        - Si la imagen supera 1 millón de píxeles, se genera una versión reducida para optimizar la visualización.
        - Guarda la imagen en `imagen_original`, `imagen_base` e `imagen`, según corresponda.
        - Inicializa el historial de deshacer/rehacer (`historial`, `redo_stack`).
        - Ajusta el tamaño máximo del historial dinámicamente en función del tamaño de la imagen.
        - Restablece el factor de zoom a 1.0 y actualiza la visualización llamando a `mostrarImagen()`.
        - Actualiza la barra de ruta con la ubicación del archivo cargado.

        Notas:
        - Si la imagen es muy grande (>1M píxeles), se calcula un factor de reducción para generar una versión optimizada.
        - `usar_version_reducida` y `factor_reduccion` se configuran para indicar si se está usando la versión reducida.
        - El tamaño del historial de deshacer se ajusta dinámicamente para evitar uso excesivo de memoria.
        """
        
        if filePath:
            # lectura de imagen y se guarda en variables a usar para la imagen
            self.imagen_original = lm.cargar_imagen(filePath)
            
            # Crear versión para UI (reducida si la imagen es grande)
            h, w = self.imagen_original.shape[:2]
            total_pixels = h * w
            
            # Si la imagen tiene más de 1 millón de píxeles, crear versión reducida para UI
            if total_pixels > 1000000:  # Umbral de 1M píxeles (ajustable)
                # Calcular factor para reducir a aprox. 1M píxeles
                factor = np.sqrt(1000000 / total_pixels)
                self.imagen_base = lm.redimensionar_imagen(self.imagen_original, factor)
                self.usar_version_reducida = True
                self.factor_reduccion = factor
            else:
                self.imagen_base = self.imagen_original.copy()
                self.usar_version_reducida = False
                self.factor_reduccion = 1.0
                
            self.imagen = self.imagen_base.copy()
            
            # inicializa los valores del undo/redo
            self.historial = [self.imagen.copy()]  # Iniciar historial con la imagen
            self.redo_stack.clear()  # Limpiar pila de rehacer
            
            # Limitar tamaño del historial basado en tamaño de imagen
            self.max_history = max(5, int(10000000 / total_pixels))  # Más pequeño para imágenes grandes
            
            # reinicia el zoom y muestra la imagen
            self.zoom_factor = 1.0 
            self.mostrarImagen()
            
            # Actualiza la barra de ruta con la ruta del archivo
            self.barraRuta.setText(filePath)
            
    def cargarImagenSecundaria(self, filePath):
        """
        Carga una imagen secundaria desde la ruta especificada para ser usada en la fusión.
        
        Args:
            filePath (str): Ruta del archivo de la imagen secundaria a cargar.
            
        Acciones:
            - Carga la imagen desde la ruta proporcionada y la almacena como imagen_secundaria.
            - Guarda una copia como imagen_secundaria_original para manipulaciones posteriores.
            - Guarda la ruta de la imagen secundaria para referencia.
            - Aplica automáticamente una fusión inicial con la imagen principal para mostrar 
              la imagen secundaria encima.
        """
        if filePath and self.imagen_base is not None:
            # Cargar la imagen secundaria
            self.imagen_secundaria = lm.cargar_imagen(filePath)
            # Guardar una copia para uso en redimensionamiento
            self.imagen_secundaria_original = self.imagen_secundaria.copy()
            self.ruta_imagen_secundaria = filePath
            
            # Aplicar una fusión inicial para mostrar la imagen secundaria encima de la principal
            # Alpha 0.7 para que se vea bien la imagen secundaria encima
            self.imagen = lm.fusionar_imagenes(self.imagen_base, self.imagen_secundaria, 
                                               alpha=0.7, x_offset=0, y_offset=0)
            
            # Guardamos en el historial y actualizamos la visualización
            self.guardarEnHistorial()
            self.mostrarImagen()
    
    def mostrarImagen(self):
        """
        Muestra la imagen actual en el QLabel de la interfaz.
        Este método toma la imagen almacenada en el atributo `self.imagen`, la convierte 
        en un formato compatible con PyQt (QImage) y la muestra en el QLabel `self.labelImagen`. 
        La imagen se escala para ajustarse al tamaño del QLabel manteniendo la relación de aspecto.
        Maneja imágenes en escala de grises, RGB y RGBA. Si la imagen no tiene un formato compatible, 
        el método no realiza ninguna acción.
        Requisitos:
        - La imagen debe estar normalizada en el rango [0, 1] antes de ser pasada a este método.
        - La biblioteca NumPy debe estar disponible.
        - Los módulos de PyQt5/PySide2 deben estar importados.
        Atributos:
        - `self.imagen`: numpy.ndarray
            Imagen actual a mostrar. Puede ser en escala de grises (2D) o con canales de color (3D).
        - `self.labelImagen`: QLabel
            Componente de la interfaz donde se mostrará la imagen.
        Excepciones:
        - Si `self.imagen` es None, el método no realiza ninguna acción.
        """
        # Verifica si hay una imagen disponible para mostrar
        if self.imagen is not None:
            # Convierte la imagen de rango [0,1] a rango [0,255] y cambia el tipo a entero de 8 bits sin signo
            img = (self.imagen * 255).astype(np.uint8)
            
            # Detecta el tipo de imagen según sus dimensiones y crea el objeto QImage correspondiente
            if len(img.shape) == 2:
                # Imagen en escala de grises (2 dimensiones: alto y ancho)
                h, w = img.shape
                qImg = QImage(img.data, w, h, w, QImage.Format.Format_Grayscale8)
            elif img.shape[2] == 3:
                # Imagen RGB (3 dimensiones: alto, ancho y 3 canales de color)
                h, w, c = img.shape
                # Asegura que los datos de la imagen estén contiguos en memoria para evitar problemas
                img = np.ascontiguousarray(img)
                bytesPerLine = 3 * w  # Calcula bytes por línea: 3 bytes (RGB) * ancho
                qImg = QImage(img.data, w, h, bytesPerLine, QImage.Format.Format_RGB888)
            elif img.shape[2] == 4:
                # Imagen RGBA (3 dimensiones: alto, ancho y 4 canales incluyendo transparencia)
                h, w, c = img.shape
                img = np.ascontiguousarray(img)
                bytesPerLine = 4 * w  # Calcula bytes por línea: 4 bytes (RGBA) * ancho
                qImg = QImage(img.data, w, h, bytesPerLine, QImage.Format.Format_RGBA8888)
            else:
                # Si el formato de la imagen no es compatible, termina la función
                return
            
            
            pixmap = QPixmap.fromImage(qImg) # Convierte QImage a QPixmap para mostrarla en un QLabel            
            label_size = self.labelImagen.size() # Obtiene el tamaño actual del QLabel
            # Escala la imagen para ajustarse al QLabel manteniendo la proporción y con transformación suave
            scaled_pixmap = pixmap.scaled(label_size, Qt.AspectRatioMode.KeepAspectRatio, 
                                        Qt.TransformationMode.SmoothTransformation)            
            self.labelImagen.setPixmap(scaled_pixmap) # Establece la imagen escalada en el QLabel            
            self.labelImagen.setAlignment(Qt.AlignmentFlag.AlignCenter) # Centra la imagen en el QLabel
        
    def guardarImagen(self, filePath):
        """
        Guarda la imagen actual en la ruta de archivo especificada.
        Si hay un historial de imágenes, se guarda la última imagen del historial.
        De lo contrario, se guarda la imagen actual.
        Args:
            filePath (str): Ruta de archivo donde se guardará la imagen.
        Nota:
            - La imagen solo se guarda si existe una imagen válida (`imgGuardar`) 
              y si se proporciona una ruta de archivo válida (`filePath`).
        """

        imgGuardar = self.historial[-1] if len(self.historial) > 1 else self.imagen
        
        if imgGuardar is not None and filePath:
            lm.guardar_imagen(filePath, imgGuardar)
    
    # --------------------------------------------------
    # configuraciones historial cambios
    # --------------------------------------------------

    def deshacerCambios(self):
        """
        Revierte los cambios realizados en la imagen, volviendo al estado anterior.
        Este método permite deshacer el último cambio realizado en la imagen. 
        Si hay más de un estado en el historial, se elimina el estado actual del historial 
        y se guarda en la pila de rehacer (`redo_stack`). Luego, se restaura la imagen 
        al estado anterior en el historial y se actualiza la visualización.
        Raises:
            IndexError: Si el historial no contiene suficientes estados para deshacer.
        """        
        if len(self.historial) > 1:
            self.redo_stack.append(self.historial.pop())  # Guardar el estado actual en rehacer
            self.imagen = self.historial[-1].copy()  # Volver al estado anterior
            self.mostrarImagen()
    
    def rehacerCambios(self):
        """
        Restaura el último cambio deshecho en la imagen.
        Este método permite rehacer el último cambio que fue deshecho previamente.
        Recupera el estado más reciente de la pila de deshacer (redo_stack),
        lo asigna como la imagen actual y lo guarda nuevamente en el historial
        para mantener un registro de los cambios realizados.
        Si no hay cambios disponibles en la pila de deshacer, no realiza ninguna acción.
        Returns:
            None
        """
        if self.redo_stack:
            self.imagen = self.redo_stack.pop().copy()  # Recuperar el último estado deshecho
            self.historial.append(self.imagen.copy())  # Guardarlo en el historial nuevamente
            self.mostrarImagen()
    
    def actualizarImagen(self):
        """
        Actualiza la imagen actual en el visor.
        Este método realiza las siguientes acciones:
        - Establece la imagen actual como la imagen base.
        - Agrega una copia de la imagen actual al historial de cambios.
        - Limpia la pila de rehacer (redo_stack) para evitar inconsistencias.
        - Muestra la imagen actualizada en el visor.
        Requiere que el atributo `imagen` no sea None para ejecutar las operaciones.
        """
        if self.imagen is not None:
            self.imagen_base = self.imagen.copy()  # Establece la imagen actual como base
            self.historial = [self.imagen.copy()]  # Reemplazar todo el historial con solo la imagen actual
            self.redo_stack.clear()  # Borra rehacer para evitar inconsistencias
            self.mostrarImagen()
            
    def guardarEnHistorial(self):
        """
        Guarda la imagen actual en el historial si es diferente a la última imagen almacenada.
        Este método verifica si hay una imagen cargada y si es diferente a la última imagen 
        almacenada en el historial. Si es así, realiza una copia de la imagen actual y la 
        agrega al historial.
        Condiciones:
        - Si no hay una imagen cargada (`self.imagen` es None), no realiza ninguna acción.
        - Si la imagen actual es idéntica a la última imagen en el historial, no realiza 
          ninguna acción.
        Efectos:
        - Agrega una copia de la imagen actual al historial (`self.historial`).
        """
        if self.imagen is not None:
            if not self.historial or not np.array_equal(self.imagen, self.historial[-1]):
                self.historial.append(self.imagen.copy())  # Guarda el estado actual en historial
                self.redo_stack.clear()  # Limpia el historial de rehacer

    # --------------------------------------------------
    # manejo imagenes
    # --------------------------------------------------

    def reiniciarImagen(self):
        """
        Restaura la imagen al estado original y restablece los parámetros de edición.

        Este método realiza las siguientes acciones:
        - Restaura la imagen actual a una copia de la imagen original.
        - Si la imagen es grande y `usar_version_reducida` está habilitado, recrea la versión optimizada.
        - Actualiza la imagen base con la copia restaurada.
        - Reinicia el historial de modificaciones con la imagen restaurada.
        - Vacía la pila de acciones de rehacer (`redo_stack`).
        - Restablece el factor de zoom a su valor predeterminado (1.0).
        - Llama al método `mostrarImagen()` para actualizar la visualización.

        Requisitos:
        - `self.imagen_original` no debe ser `None` para realizar la restauración.
        - Si `usar_version_reducida` está definido y activado, se aplicará la función `lm.redimensionar_imagen()`.

        """
        if self.imagen_original is not None:
            # Utilizar la versión optimizada si es una imagen grande
            if hasattr(self, 'usar_version_reducida') and self.usar_version_reducida:
                # Recrear la versión optimizada usando el mismo factor
                self.imagen = lm.redimensionar_imagen(self.imagen_original, self.factor_reduccion)
                self.imagen_base = self.imagen.copy()
            else:
                # Para imágenes pequeñas, usar directamente la original
                self.imagen = self.imagen_original.copy()
                self.imagen_base = self.imagen.copy()
                
            # Reiniciar historial y otros parámetros
            self.historial = [self.imagen.copy()]
            self.redo_stack.clear()
            self.zoom_factor = 1.0
            self.mostrarImagen()

    def rotornarHastaImagenBase(self):
        """
        Restaura la imagen actual a su estado base.
        Este método verifica si existe una imagen base cargada. Si es así, 
        restablece la imagen actual a una copia de la imagen base, actualiza 
        el historial con la imagen base y actualiza la visualización de la imagen.
        Returns:
            None
        """

        if self.imagen_base is not None:
            self.imagen = self.imagen_base.copy()
            self.historial.append(self.imagen.copy())
            self.mostrarImagen()


    def aplicarAjusteBrillo(self, valor):
        """
        Aplica un ajuste de brillo a la imagen base utilizando el valor proporcionado.
        Args:
            valor (float): Valor del ajuste de brillo a aplicar. Puede ser positivo 
            para aumentar el brillo o negativo para disminuirlo.
        Acciones:
            - Modifica la imagen actual aplicando el ajuste de brillo a partir de la imagen base.
            - Guarda el estado actual de la imagen en el historial.
            - Muestra la imagen ajustada en la interfaz.
        """
        if self.imagen_base is not None:
            self.imagen = lm.ajusteBrillo(self.imagen_base, valor)
            self.guardarEnHistorial() 
            self.mostrarImagen()

    def ajustarContrastePositivo(self, valor):
        """
        Ajusta el contraste de la imagen base incrementándolo en función del valor proporcionado.
        Args:
            valor (float): Valor que determina el nivel de ajuste positivo del contraste.
                           Valor entre 0.0 y 1.0, donde 1.0 representa sin cambios.
        Acciones:
            - Si el valor es 1.0 (o muy cercano), muestra la imagen base sin cambios.
            - De lo contrario, aplica un ajuste positivo de contraste a la imagen base.
            - Guarda el estado actual de la imagen en el historial.
            - Muestra la imagen ajustada en la interfaz.
        Nota:
            Este método no realiza ninguna acción si `imagen_base` es None.
        """
        
        if self.imagen_base is not None:
            # Si el valor es 1.0 (slider al máximo), mostrar la imagen original
            if valor >= 0.99:  # Usar 0.99 para manejar posibles imprecisiones numéricas
                self.imagen = self.imagen_base.copy()
            else:
                # Aplicar el ajuste de contraste normalmente
                self.imagen = lm.ajusteContraste(self.imagen_base, valor, 1)
                
            self.guardarEnHistorial() 
            self.mostrarImagen()

    def ajustarContrasteNegativo(self, valor):
        """
        Ajusta el contraste de la imagen actual aplicando un valor negativo.
        Args:
            valor (float): Valor para ajustar el contraste de la imagen.
                           Valor entre 0.0 y 1.0, donde 1.0 representa sin cambios.
        Acciones:
            - Si el valor es 1.0 (o muy cercano), muestra la imagen base sin cambios.
            - De lo contrario, aplica un ajuste negativo de contraste a la imagen base.
            - Guarda el estado actual de la imagen en el historial.
            - Muestra la imagen ajustada en la interfaz.
        Nota:
            Este método no realiza ninguna acción si no hay una imagen base cargada.
        """
        
        if self.imagen_base is not None:
            # Si el valor es 1.0 (slider al máximo), mostrar la imagen original
            if valor >= 0.99:  # Usar 0.99 para manejar posibles imprecisiones numéricas
                self.imagen = self.imagen_base.copy()
            else:
                # Aplicar el ajuste de contraste normalmente
                self.imagen = lm.ajusteContraste(self.imagen_base, valor, 0)
                
            self.guardarEnHistorial() 
            self.mostrarImagen()

    def invertirColoresImagen(self):
        """
        Invierte los colores de la imagen actual.
        Este método aplica una inversión de colores a la imagen base cargada 
        y actualiza la imagen mostrada en la interfaz. Además, guarda la 
        imagen modificada en el historial para permitir deshacer cambios.
        Requiere:
            - Que la propiedad `imagen_base` no sea None, es decir, que 
              exista una imagen cargada previamente.
        Acciones:
            - Invierte los colores de la imagen base utilizando la función 
              `lm.invertirColoresImagen`.
            - Guarda la imagen modificada en el historial mediante 
              `guardarEnHistorial`.
            - Actualiza la interfaz para mostrar la imagen modificada 
              utilizando `mostrarImagen`.
        """
        
        if self.imagen is not None:
            self.imagen = lm.invertirColoresImagen(self.imagen)
            # self.imagen = self.imagen.copy() # Actualizar base modificada
            self.guardarEnHistorial() 
            self.mostrarImagen()    

    def binarizarImagen(self):
        """
        Binariza la imagen actual utilizando la función `binarizar_imagen` del módulo `lm`.
        Este método verifica si existe una imagen base cargada. Si es así, aplica un proceso
        de binarización a la imagen base, guarda el resultado en el historial y actualiza
        la visualización de la imagen.
        Returns:
            None
        """
        
        if self.imagen_base is not None:
            self.imagen = lm.binarizar_imagen(self.imagen_base)
            self.guardarEnHistorial() 
            self.mostrarImagen()
    
    def aplicarRotacion(self, angulo):
        """
        Aplica una rotación a la imagen base según el ángulo especificado.
        Args:
            angulo (float): Ángulo en grados para rotar la imagen. 
                            Los valores positivos rotan en sentido antihorario 
                            y los negativos en sentido horario.
        Acciones:
            - Rota la imagen base utilizando la función `lm.rotar_imagen`.
            - Guarda el estado actual de la imagen en el historial.
            - Muestra la imagen rotada en la interfaz.
        """
        
        if self.imagen_base is not None:
            self.imagen = lm.rotar_imagen(self.imagen_base, angulo)
            self.guardarEnHistorial() 
            self.mostrarImagen()

    def aplicarCapaImagen(self, imagen_capa):
        """
        Aplica una capa de imagen sobre la imagen base actual.
        Args:
            imagen_capa: La capa de imagen que se aplicará sobre la imagen base.
        Acciones:
            - Combina la imagen base con la capa proporcionada utilizando la función `lm.capaImagen`.
            - Guarda el estado actual de la imagen en el historial.
            - Muestra la imagen resultante en la interfaz de usuario.
        Nota:
            Este método no realiza ninguna acción si `self.imagen_base` es None.
        """
        if self.imagen_base is not None:
            self.imagen = lm.capaImagen(self.imagen_base, imagen_capa)
            self.guardarEnHistorial()
            self.mostrarImagen()
    
    def aplicarQuitarCanal(self, canal):
        """
        Aplica o quita un canal de color de la imagen base y actualiza la imagen mostrada.
        Args:
            canal (str): El canal de color a quitar de la imagen. Puede ser 'R', 'G' o 'B' 
                 para los canales rojo, verde o azul, respectivamente.
        Comportamiento:
            - Si existe una imagen base (`imagen_base`), se elimina el canal especificado 
              utilizando la función `quitarCanal`.
            - Guarda el estado actual de la imagen en el historial mediante `guardarEnHistorial`.
            - Actualiza la visualización de la imagen llamando a `mostrarImagen`.
        """
        if self.imagen_base is not None:
            self.imagen = lm.quitarCanal(self.imagen_base, canal)
            self.guardarEnHistorial() 
            self.mostrarImagen()
        
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
            self.guardarEnHistorial()       
            self.mostrarImagen()            

    def mostrarHistograma(self):
        """
        Muestra el histograma de la imagen actual.
        Este método verifica si hay una imagen cargada en el atributo `self.imagen`.
        Si existe, llama a la función `histograma_imagen` del módulo `lm` para
        generar y mostrar el histograma de la imagen.
        Returns:
            None
        """
        
        if self.imagen is not None:
            lm.histograma_imagen(self.imagen)
    
    def aplicarZoom(self, factor, cursor_x=None, cursor_y=None):
        """
        Aplica un zoom a la imagen actual basada en un factor de escala y una posición opcional del cursor.
        Args:
            factor (float): Factor de escala para el zoom. Valores mayores a 1 aumentan el zoom, 
                            mientras que valores entre 0 y 1 lo disminuyen.
            cursor_x (int, opcional): Coordenada X del cursor para centrar el zoom. 
                                      Si no se proporciona, se utiliza el centro de la imagen.
            cursor_y (int, opcional): Coordenada Y del cursor para centrar el zoom. 
                                      Si no se proporciona, se utiliza el centro de la imagen.
        Notas:
            - El factor de zoom se limita a un rango entre 0.1 y 5.0.
            - La imagen se actualiza aplicando el zoom y se guarda en el historial.
            - Finalmente, se muestra la imagen actualizada.
        """
        
        if self.imagen is not None and self.imagen_base is not None:
            h, w = self.imagen.shape[:2]
            
            # Si no se proporciona posición, usar el centro de la imagen
            if cursor_x is None or cursor_y is None:
                cursor_x, cursor_y = w // 2, h // 2  # Zoom centrado si no se proporciona posición
            
            # Actualizar el factor de zoom global
            nuevo_zoom_factor = self.zoom_factor * factor
            
            # Limitar el zoom entre 0.1 (10%) y 5.0 (500%)
            nuevo_zoom_factor = max(0.1, min(nuevo_zoom_factor, 5.0))
            
            # Eliminar la condición de igualdad exacta para evitar problemas de precisión
            # y siempre aplicar el zoom cuando se llama a esta función
            self.zoom_factor = nuevo_zoom_factor            
            
            # Aplicar el zoom usando la librería de manipulación
            self.imagen = lm.aplicar_zoom(self.imagen_base, self.zoom_factor, cursor_x, cursor_y)
            self.guardarEnHistorial() 
            self.mostrarImagen()

    def setZoomCombo(self, zoom_text, cursor_x=None, cursor_y=None):
        """
        Ajusta el nivel de zoom de la imagen y actualiza su visualización.
        Args:
            zoom_text (str): Texto que representa el nivel de zoom en porcentaje 
                (por ejemplo, "120%"). Si no se puede convertir, se usará un valor 
                por defecto de 100%.
            cursor_x (int, opcional): Coordenada X del cursor para centrar el zoom. 
                Si no se proporciona, se usará el centro de la imagen.
            cursor_y (int, opcional): Coordenada Y del cursor para centrar el zoom. 
                Si no se proporciona, se usará el centro de la imagen.
        Comportamiento:
            - Convierte el texto del zoom en un factor numérico.
            - Si no se proporciona una posición del cursor, se toma el centro de la imagen.
            - Aplica el zoom a la imagen utilizando el factor calculado y las coordenadas 
              del cursor.
            - Actualiza la visualización de la imagen con el nuevo nivel de zoom.
        """
        
        if self.imagen is None:
            return
            
        # Extraer el valor numérico y convertir a factor (por ejemplo, "120%" -> 1.2)
        try:
            zoom_value = int(zoom_text.replace("%", ""))
        except ValueError:
            zoom_value = 100  # valor por defecto si falla la conversión
        
        factor = zoom_value / 100.0  # 1.0 es tamaño normal

        h, w = self.imagen.shape[:2]
        # Si no se provee la posición, se toma el centro de la imagen
        if cursor_x is None or cursor_y is None:
            cursor_x, cursor_y = w // 2, h // 2
            
        # Reemplazar factor actual en vez de multiplicarlo
        self.zoom_factor = factor        
        
        # Aplicar zoom desde la imagen base, no la actual
        self.imagen = lm.aplicar_zoom(self.imagen_base, self.zoom_factor, cursor_x, cursor_y)
        self.guardarEnHistorial()
        self.mostrarImagen()


    # -------------------------------------------------
    # Funciones para la opción de Fusionar Imagenes
    # -------------------------------------------------   
    def aplicarFusionImagenes(self, imagen_secundaria, alpha=0.5, x_offset=0, y_offset=0):
        """
        Fusiona la imagen base con una imagen secundaria superpuesta.
        
        Args:
            imagen_secundaria (numpy.ndarray): La imagen que se superpondrá sobre la imagen base.
            alpha (float, opcional): Nivel de transparencia de la imagen superpuesta. 
                                    Valores entre 0 (completamente transparente) y 1 (completamente opaca). 
                                    Por defecto es 0.5.
            x_offset (int, opcional): Desplazamiento horizontal (en píxeles) desde la esquina superior 
                                     izquierda donde se colocará la imagen superpuesta. Por defecto es 0.
            y_offset (int, opcional): Desplazamiento vertical (en píxeles) desde la esquina superior 
                                     izquierda donde se colocará la imagen superpuesta. Por defecto es 0.
                                     
        Acciones:
            - Verifica si existe una imagen base.
            - Utiliza la función lm.fusionar_imagenes para superponer la imagen secundaria sobre la imagen base.
            - Guarda el resultado en el historial y actualiza la visualización.
        """
        if self.imagen_base is not None and imagen_secundaria is not None:
            # Fusionar las imágenes usando la función de la librería de manipulación
            self.imagen = lm.fusionar_imagenes(self.imagen_base, imagen_secundaria, alpha, x_offset, y_offset)
            self.guardarEnHistorial()
            self.mostrarImagen()
    
    def redimensionarImagenSecundaria(self, factor):
        """
        Redimensiona la imagen secundaria según el factor especificado.
        
        Args:
            factor (float): Factor de escala para redimensionar la imagen secundaria.
                            Por ejemplo, 0.5 para reducir a la mitad, 2.0 para duplicar el tamaño.
        
        Acciones:
            - Redimensiona la imagen secundaria usando la función redimensionar_imagen de la librería.
            - Actualiza la variable imagen_secundaria con la versión redimensionada.
        """
        if self.imagen_secundaria is not None:
            try:
                # Guardamos la imagen secundaria original si no existe o es None
                if not hasattr(self, 'imagen_secundaria_original') or self.imagen_secundaria_original is None:
                    self.imagen_secundaria_original = self.imagen_secundaria.copy()
                
                # Usar la función de la librería de manipulación para redimensionar
                # partiendo siempre de la imagen original para evitar degradación acumulativa
                self.imagen_secundaria = lm.redimensionar_imagen(self.imagen_secundaria_original, factor)
                
                # Informar sobre el cambio (opcional)
                h, w = self.imagen_secundaria.shape[:2]                
                
            except Exception as e:
                print(f"Error al redimensionar: {e}")
                return
    
    def restaurarImagenBase(self):
        """
        Restaura la imagen a su estado base, descartando temporalmente la fusión con la imagen secundaria.
        
        Esta función no elimina la imagen secundaria, solo restaura la imagen actualmente
        mostrada a su estado base, permitiendo volver a aplicar la fusión posteriormente.
        """
        if self.imagen_base is not None:
            # Restaurar la imagen actual a partir de la imagen base
            self.imagen = self.imagen_base.copy()
            
            # Mostrar la imagen base sin la fusión
            self.mostrarImagen()
