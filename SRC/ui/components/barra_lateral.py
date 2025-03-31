from PyQt6.QtWidgets import ( 
    QToolBar, QComboBox, QDial, QPushButton, QDockWidget, QWidget, QLabel, QVBoxLayout, QSlider, QFrame,
    QHBoxLayout, QVBoxLayout, QLineEdit
)
from PyQt6.QtGui import QIcon, QAction, QActionGroup
from PyQt6.QtCore import QSize, Qt
import config.config as cfg

class BarraLateral(QToolBar):
    
    def __init__(self, parent):
        """
        Inicializa una instancia de la clase BarraLateral.
        Args:
            parent (QMainWindow): Referencia al widget principal (QMainWindow) que actúa como padre.
        Atributos:
            parent (QMainWindow): Guarda la referencia al QMainWindow principal.
            dock_widget (QDockWidget): Dock widget utilizado para mostrar las opciones, 
                fijado al área derecha y oculto inicialmente.
            widgetOpciones (QWidget): Widget contenedor para las opciones dentro del dock widget.
            layoutOpciones (QVBoxLayout): Layout vertical para organizar los elementos dentro del widget de opciones.
        Acciones:
            - Configura la orientación de la barra lateral como vertical.
            - Establece el tamaño de los íconos en 32x32 píxeles.
            - Crea y configura un QDockWidget para mostrar opciones adicionales.
            - Añade el dock widget al QMainWindow padre en el área derecha.
            - Inicializa los botones de acción llamando al método `initActions`.
        """
        
        super().__init__("Barra lateral")
        self.setOrientation(Qt.Orientation.Vertical)
        self.setIconSize(QSize(32, 32))

        self.parent = parent  # Guardamos referencia al `QMainWindow`
        
        # Crear el dock widget para mostrar las opciones
        self.dock_widget = QDockWidget("Opciones", parent)
        self.dock_widget.setAllowedAreas(Qt.DockWidgetArea.RightDockWidgetArea)  # Fijado a la derecha
        self.dock_widget.setVisible(False)  # Oculto al inicio

        self.widgetOpciones = QWidget()
        self.layoutOpciones = QVBoxLayout(self.widgetOpciones)

        parent.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_widget)
        
        # Botones de acción
        self.initActions()

    def initActions(self):
        """
        Inicializa las acciones de la barra lateral y las agrupa en un QActionGroup.
        Este método configura tres botones en la barra lateral: "Ajustes Básicos", 
        "Ajustes de Filtros" y "Ajustes Avanzados". Cada botón tiene un ícono, un 
        texto descriptivo y está asociado a una acción específica. Además, las 
        acciones son agrupadas en un QActionGroup para que solo una de ellas pueda 
        estar activada al mismo tiempo.
        Acciones configuradas:
        - "Ajustes Básicos": Muestra las opciones básicas al ser activada.
        - "Ajustes de Filtros": Muestra las opciones de filtros al ser activada.
        - "Ajustes Avanzados": Muestra las opciones avanzadas al ser activada.
        Métodos conectados:
        - Cada acción está conectada al método `mostrarOpciones` con un argumento 
          que indica el tipo de opciones a mostrar.
        Notas:
        - Los íconos de las acciones se obtienen de la configuración `cfg.ICONOS`.
        - Las acciones son añadidas al contexto del widget y al grupo de acciones 
          para garantizar su exclusividad.
        """
        action_group = QActionGroup(self)  # Crear un grupo para las acciones
        action_group.setExclusive(True)  # Solo una acción puede estar activada a la vez

        # configuracion para el btn de los ajustes basicos que se encuentra en la barra lateral
        ajustes_basicos_icon_path = cfg.ICONOS["ajustesBasicos"]
        ajustes_basicos_action = QAction(QIcon(ajustes_basicos_icon_path), "Ajustes Básicos", self)
        ajustes_basicos_action.setCheckable(True)  
        ajustes_basicos_action.triggered.connect(lambda: self.mostrarOpciones("Básicos"))
        self.addAction(ajustes_basicos_action)
        action_group.addAction(ajustes_basicos_action) 

        # configuracion para el btn de los ajustes de filtros que se encuentra en la barra lateral
        ajustes_filtros_icon_path = cfg.ICONOS["ajustesDeFiltros"]
        ajustes_filtros_action = QAction(QIcon(ajustes_filtros_icon_path), "Ajustes de Filtros", self)
        ajustes_filtros_action.setCheckable(True)  
        ajustes_filtros_action.triggered.connect(lambda: self.mostrarOpciones("de Filtros"))
        self.addAction(ajustes_filtros_action)
        action_group.addAction(ajustes_filtros_action)  

        # configuracion para el btn de los ajustes avanzados que se encuentra en la barra lateral
        ajustes_avanzados_icon_path = cfg.ICONOS["ajustesAvanzados"]
        ajustes_avanzados_action = QAction(QIcon(ajustes_avanzados_icon_path), "Ajustes Avanzados", self)
        ajustes_avanzados_action.setCheckable(True)  
        ajustes_avanzados_action.triggered.connect(lambda: self.mostrarOpciones("Avanzados"))
        self.addAction(ajustes_avanzados_action)
        action_group.addAction(ajustes_avanzados_action) 

    def mostrarOpciones(self, tipo):
        """
        Muestra y configura las opciones en el panel lateral (dock widget) según el tipo especificado.
        Este método gestiona la visibilidad y el contenido del panel lateral, permitiendo
        mostrar diferentes configuraciones dependiendo del tipo seleccionado. Si el panel
        ya está visible con las opciones del mismo tipo, se oculta. Si no, se actualiza
        con las nuevas opciones correspondientes al tipo.
        Args:
            tipo (str): El tipo de opciones a mostrar en el panel lateral. Puede ser:
                - "Básicos": Para mostrar las opciones básicas.
                - "de Filtros": Para mostrar las opciones relacionadas con filtros.
                - "Avanzados": Para mostrar las opciones avanzadas.
        Comportamiento:
            - Si el panel lateral ya está visible con las opciones del mismo tipo, se oculta.
            - Si el panel lateral está visible con otro tipo de opciones, se reemplaza su contenido.
            - Se crean widgets dinámicamente para mostrar las opciones correspondientes al tipo.
            - Se ajusta el tamaño mínimo del panel lateral y su contenido.
        Notas:
            - Este método utiliza `self.sender()` para identificar la acción que activó la señal.
            - Los widgets previos en el panel lateral se eliminan antes de agregar los nuevos.
            - Los métodos `configurarOpcionesBasicas`, `configurarOpcionesFiltros` y 
              `configurarOpcionesAvanzadas` son responsables de agregar las opciones específicas
              al layout proporcionado.
        """
        
        sender_action = self.sender()  # Obtener la acción que activó la señal

        if self.dock_widget.isVisible() and self.dock_widget.windowTitle() == f"Ajustes {tipo}":
            self.dock_widget.setVisible(False)  # Ocultar si ya está abierto con la misma opción
            if sender_action:
                sender_action.setChecked(False)  # Desmarcar el botón
            return

        # Limpiar cualquier widget previo en el dock
        for i in reversed(range(self.layoutOpciones.count())):
            # widget_to_remove = self.layoutOpciones.itemAt(i).widget()
            widget_to_remove = self.layoutOpciones.takeAt(i).widget()
            if widget_to_remove is not None:
                widget_to_remove.deleteLater()

        # Crear el nuevo widget con las opciones
        widget_opciones = QWidget()
        layout = QVBoxLayout(widget_opciones)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Ajustar tamaño del widget
        widget_opciones.setMinimumSize(250, 400)  # Ancho: 250px, Alto: 400px
        self.dock_widget.setMinimumSize(250, 400)  # También aplicarlo al DockWidget para que crezca
        self.dock_widget.setVisible(True)  # Mostrar el panel                
        
        # aca se agregan las opciones del menu lateral de los ajustes basicos
        if tipo == "Básicos":
            self.configurarOpcionesBasicas(layout)
        
        # aca se agregan las opciones del menu lateral de los ajustes de filtros
        if tipo == "de Filtros" :
            self.configurarOpcionesFiltros(layout)
            
        # aca se agregan las opciones del menu lateral de los ajustes avanzados
        if tipo == 'Avanzados':
            self.configurarOpcionesAvanzadas(layout)
            
        # se agregan las opciones configuradas al layout del widget
        widget_opciones.setLayout(layout)

        # Establecer el nuevo widget en el dock
        self.dock_widget.setWidget(widget_opciones)
        self.dock_widget.setWindowTitle(f"Ajustes {tipo}")  # Guardar el título para verificar estado
        self.dock_widget.setVisible(True)  # Mostrar el dock widget
    
    def configurarSeparador(self):
        """
        Configura y devuelve un separador visual.
        Este método crea un objeto QFrame que actúa como un separador horizontal
        con un estilo de línea hundida (Sunken). Es útil para dividir visualmente
        secciones en una interfaz de usuario.
        Returns:
            QFrame: Un objeto QFrame configurado como separador horizontal.
        """
        
        # Separador visual
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        return separator 

    def configurarOpcionesBasicas(self, layout):
        """
        Configura las opciones básicas de la barra lateral en la interfaz de usuario.
        Este método agrega varios controles interactivos al layout proporcionado, 
        incluyendo sliders para ajustar brillo y contraste, un combo box y un dial 
        para controlar la rotación de la imagen. Los controles están diseñados para 
        interactuar con un visor de imágenes asociado.
        Args:
            layout (QLayout): El layout principal donde se agregarán los controles.
        Controles agregados:
            - Separadores visuales para organizar los elementos.
            - Slider de brillo:
                * Permite ajustar el brillo de la imagen.
                * Rango: 1 a 200 (100 es el valor neutral).
            - Slider de contraste negativo:
                * Permite ajustar el contraste negativo de la imagen.
                * Rango: 1 a 100 (1 es el valor neutral).
            - Slider de contraste positivo:
                * Permite ajustar el contraste positivo de la imagen.
                * Rango: 1 a 100 (100 es el valor neutral).
            - Controles de rotación:
                * Combo box con ángulos notables predefinidos.
                * Dial para ajuste manual de la rotación en un rango de -180° a 180°.
        Notas:
            - Los sliders y controles están conectados a métodos del visor de imágenes 
              para aplicar los ajustes en tiempo real.
            - El método verifica que el layout tenga el método `addWidget` y que el 
              objeto padre tenga un atributo `visor` antes de agregar los controles.
        """
        
        if hasattr(layout, 'addWidget') and hasattr(self.parent, 'visor'):
            
            # -------------------------------------------------
            # se agrega un separador visual
            # -------------------------------------------------
            layout.addWidget(self.configurarSeparador())
            
            # -------------------------------------------------
            # **Slider de Brillo**
            # -------------------------------------------------
            # Contenedor vertical para el slider y etiquetas
            brillo_layout = QVBoxLayout()

            # Etiqueta de título
            lbl_titulo = QLabel("Brillo")
            brillo_layout.addWidget(lbl_titulo)

            # Layout horizontal para el slider y valores
            slider_layout = QHBoxLayout()
            
            lbl_min = QLabel("-")  # Límite izquierdo
            lbl_min.setAlignment(Qt.AlignmentFlag.AlignLeft)

            lbl_max = QLabel("+")  # Límite derecho
            lbl_max.setAlignment(Qt.AlignmentFlag.AlignRight)

            self.slider_brillo = QSlider(Qt.Orientation.Horizontal)
            self.slider_brillo.setMinimum(1)
            self.slider_brillo.setMaximum(200)  # 100 = valor neutral (1.0)
            self.slider_brillo.setValue(100)  # Valor inicial (1.0)
            self.slider_brillo.setTickInterval(10)
            self.slider_brillo.setSingleStep(1)
            
            # Conectar evento usando una función en lugar de lambda
            self.slider_brillo.valueChanged.connect(lambda val: self.parent.visor.aplicarAjusteBrillo(self.cambiarValorSlider(val)))

            # Agregar widgets al layout horizontal
            slider_layout.addWidget(lbl_min)
            slider_layout.addWidget(self.slider_brillo)
            slider_layout.addWidget(lbl_max)

            # # Agregar el slider al layout vertical
            brillo_layout.addLayout(slider_layout)

            # Agregar el control completo al layout principal
            layout.addLayout(brillo_layout)

            # -------------------------------------------------
            # se agrega un separador visual
            # -------------------------------------------------
            layout.addWidget(self.configurarSeparador())
            
            # -------------------------------------------------
            # 🔹 Slider para contraste negativo
            # -------------------------------------------------
            layout.addWidget(QLabel("Contraste"))
            
            self.sliderContrasteNegativo = QSlider(Qt.Orientation.Horizontal)
            self.sliderContrasteNegativo.setMinimum(1)   # Equivalente a 0.01
            self.sliderContrasteNegativo.setMaximum(100)  # Equivalente a 1.0
            self.sliderContrasteNegativo.setValue(1)    # Neutro = 0.01
            self.sliderContrasteNegativo.setSingleStep(1)
            self.sliderContrasteNegativo.valueChanged.connect(lambda val: self.parent.visor.ajustarContrasteNegativo(self.cambiarValorSlider(val)))

            layout.addWidget(QLabel("negativo"))
            layout.addWidget(self.sliderContrasteNegativo)
            
            # -------------------------------------------------
            # 🔹 Slider para contraste positivo
            # -------------------------------------------------
            self.sliderContrastePositivo = QSlider(Qt.Orientation.Horizontal)
            self.sliderContrastePositivo.setMinimum(1)   # Equivalente a 0.01
            self.sliderContrastePositivo.setMaximum(100)  # Equivalente a 1.0
            self.sliderContrastePositivo.setValue(100)    # Neutro = 1.0
            self.sliderContrastePositivo.setSingleStep(1)
            self.sliderContrastePositivo.valueChanged.connect(lambda val: self.parent.visor.ajustarContrastePositivo(self.cambiarValorSlider(val)))

            layout.addWidget(QLabel("positivo"))
            layout.addWidget(self.sliderContrastePositivo)

            # -------------------------------------------------
            # se agrega un separador visual
            # -------------------------------------------------
            layout.addWidget(self.configurarSeparador())

            # -------------------------------------------------
            # Crear el input para la rotación
            # -------------------------------------------------
            layout.addWidget(QLabel("Rotación de Imagen"))

            # Crear el combo para ángulos notables
            self.combo_rotacion = QComboBox()
            angulos_notables = [0, 30, 45, 60, 90, 120, 135, 150, 180, -30, -45, -60, -90, -120, -135, -150, -180]
            self.combo_rotacion.addItems([f"{a}°" for a in angulos_notables])

            # Crear el dial para ajuste manual
            self.dial_rotacion = QDial()
            self.dial_rotacion.setMinimum(-180)
            self.dial_rotacion.setMaximum(180)
            self.dial_rotacion.setValue(0)
            self.dial_rotacion.setSingleStep(5)

            # Función para aplicar rotación desde el combo
            def aplicarRotacionDesdeCombo():
                valor = int(self.combo_rotacion.currentText().replace("°", ""))
                self.parent.visor.aplicarRotacion(valor)

            # Conectar eventos
            self.combo_rotacion.currentIndexChanged.connect(aplicarRotacionDesdeCombo)
            self.dial_rotacion.valueChanged.connect(lambda val: self.parent.visor.aplicarRotacion(val))

            # Agregar al layout
            layout.addWidget(self.combo_rotacion)
            layout.addWidget(self.dial_rotacion)
    
    def configurarOpcionesFiltros(self, layout):
        """
        Configura las opciones de filtros en el layout proporcionado, añadiendo widgets
        interactivos para aplicar diferentes transformaciones y filtros a las imágenes.
        Parámetros:
        -----------
        layout : QLayout
            El layout donde se agregarán los widgets de configuración de filtros.
        Funcionalidad:
        --------------
        - Agrega separadores visuales para organizar los elementos en el layout.
        - Botón "Binarizar imagen":
            Permite aplicar un filtro de binarización a la imagen actual.
        - Botón "Invertir colores":
            Permite invertir los colores de la imagen actual.
        - Selección de capa RGB:
            ComboBox para seleccionar una capa de color (Rojo, Verde, Azul o todas).
            Aplica la capa seleccionada a la imagen.
        - Generar CMY:
            ComboBox para eliminar un canal de color (Cian, Magenta o Amarillo).
            Aplica la eliminación del canal seleccionado a la imagen.
        - Filtro de zonas claras/oscuras:
            - ComboBox para seleccionar el modo de filtrado (zonas claras u oscuras).
            - Slider para ajustar el umbral del filtro (0 a 100).
            - ComboBox para seleccionar el color del filtro (Rojo, Verde o Azul).
            - Botón para aplicar el filtro con los parámetros seleccionados.
        Notas:
        ------
        - Los métodos `binarizarImagen`, `invertirColoresImagen`, `reiniciarImagen`,
          `aplicarCapaImagen`, y `aplicarQuitarCanal` deben estar implementados en
          el objeto `visor` del padre (`self.parent.visor`).
        - El método `aplicarFiltroZonas` debe estar implementado en esta clase.
        """
        
        if hasattr(layout, 'addWidget') and hasattr(self.parent, 'visor'):
            
            # -------------------------------------------------
            # se agrega un separador visual
            # -------------------------------------------------
            layout.addWidget(self.configurarSeparador())
            
            # -------------------------------------------------
            # Botón "binarizar" 
            # -------------------------------------------------
            layout.addWidget(QLabel("Binarizar imagen"))
            btn_binarizar = QPushButton("Aplicar")
            btn_binarizar.clicked.connect(self.parent.visor.binarizarImagen)
            layout.addWidget(btn_binarizar)
            
            # -------------------------------------------------
            # se agrega un separador visual
            # -------------------------------------------------
            layout.addWidget(self.configurarSeparador())
            
            # -------------------------------------------------
            # Botón "Invertir colores"
            # -------------------------------------------------
            layout.addWidget(QLabel("Invertir Colores"))
            btn_invertir_color = QPushButton("Invertir")
            btn_invertir_color.clicked.connect(self.parent.visor.invertirColoresImagen)
            layout.addWidget(btn_invertir_color)
            
            # -------------------------------------------------
            # se agrega un separador visual
            # -------------------------------------------------
            layout.addWidget(self.configurarSeparador())

            # -------------------------------------------------
            # CAPAS RGB
            # -------------------------------------------------
            layout.addWidget(QLabel("Seleccionar Capa de Color"))

            # Crear el combo para seleccionar la capa
            self.combo_capa = QComboBox()
            capas = {
                "RGB (Todas)": -1,
                "Rojo": 0,
                "Verde": 1,
                "Azul": 2
            }
            self.combo_capa.addItems(capas.keys())
            self.combo_capa.setCurrentText("RGB (Todas)")
                
            # Función para aplicar la selección de capa
            def aplicarCapaSeleccionada():
                nombre_capa = self.combo_capa.currentText()
                indice_capa = capas[nombre_capa]
                if indice_capa == -1:
                    self.parent.visor.rotornarHastaImagenBase()
                else:
                    self.parent.visor.aplicarCapaImagen(indice_capa)

            # Conectar el evento de selección
            self.combo_capa.currentIndexChanged.connect(aplicarCapaSeleccionada)

            # Agregar al layout
            layout.addWidget(self.combo_capa)
            
            # -------------------------------------------------
            # CAPAS CYM
            # -------------------------------------------------
            layout.addWidget(self.configurarSeparador())

            # -------------------------------------------------
            # Botón "cmy"
            # -------------------------------------------------
            layout.addWidget(QLabel("Generar CMY"))

            # Crear el combo para seleccionar el canal a eliminar
            self.combo_eliminar_canal = QComboBox()
            canales = {
                "Ninguno": -1,  # -1 indica que no se elimina ningún canal (imagen original)
                "Cian": 0,
                "Magenta": 1,
                "Amarillo": 2
            }
            self.combo_eliminar_canal.addItems(canales.keys())
            self.combo_eliminar_canal.setCurrentText("Ninguno")  # Establecer RGB como valor inicial

            # Función para aplicar la eliminación de canal
            def aplicarQuitarCanal():
                nombre_canal = self.combo_eliminar_canal.currentText()
                indice_canal = canales[nombre_canal]
                if indice_canal == -1:
                    self.parent.visor.rotornarHastaImagenBase()
                else:
                    self.parent.visor.aplicarQuitarCanal(indice_canal)

            # Conectar el evento de selección
            self.combo_eliminar_canal.currentIndexChanged.connect(aplicarQuitarCanal)

            # Agregar al layout
            layout.addWidget(self.combo_eliminar_canal)
            
            # -------------------------------------------------
            # se agrega un separador visual
            # -------------------------------------------------
            layout.addWidget(self.configurarSeparador())
            
            # -------------------------------------------------
            # FILTRO DE ZONAS
            # -------------------------------------------------
            # Sección para filtrar zonas claras u oscuras
            layout.addWidget(QLabel("Filtrar Zonas Claras/Oscuras"))

            # Combo para seleccionar el modo ('claras' o 'oscuras')
            self.combo_modoFiltro = QComboBox()
            self.combo_modoFiltro.addItems(["claras", "oscuras"])
            layout.addWidget(QLabel("Modo"))
            layout.addWidget(self.combo_modoFiltro)

            # Slider para definir el umbral (0 a 100, que luego se normaliza)
            self.slider_umbral = QSlider(Qt.Orientation.Horizontal)
            self.slider_umbral.setMinimum(0)
            self.slider_umbral.setMaximum(100)
            self.slider_umbral.setValue(50)  # Umbral por defecto 0.5
            self.slider_umbral.setTickInterval(10)
            self.slider_umbral.setSingleStep(1)
            layout.addWidget(QLabel("Umbral"))
            layout.addWidget(self.slider_umbral)

            # Combo para seleccionar el color del filtro
            self.combo_colorFiltro = QComboBox()
            # Definimos algunas opciones de color (puedes extender esta lista)
            colores = {"Rojo": "[1, 0, 0]", "Verde": "[0, 1, 0]", "Azul": "[0, 0, 1]"}
            self.combo_colorFiltro.addItems(list(colores.keys()))
            layout.addWidget(QLabel("Color del filtro"))
            layout.addWidget(self.combo_colorFiltro)

            # Botón para aplicar el filtro
            btn_aplicarFiltro = QPushButton("Aplicar Filtro")
            btn_aplicarFiltro.clicked.connect(lambda: self.aplicarFiltroZonas())
            layout.addWidget(btn_aplicarFiltro)
            
    def configurarOpcionesAvanzadas(self, layout):
        """
        Configura las opciones avanzadas en el diseño proporcionado, añadiendo widgets interactivos
        para realizar diversas operaciones sobre la imagen mostrada en el visor.
        Args:
            layout (QLayout): El diseño donde se agregarán los widgets.
        Widgets añadidos:
            - Separadores visuales para organizar los elementos.
            - Botón "Mostrar Histograma": Muestra el histograma de la imagen actual.
            - ComboBox "Zoom de Imagen": Permite seleccionar un nivel de zoom entre 100% y 300%.
            - Botón "Borrar modificaciones": Restaura la imagen a su estado original.
        Notas:
            - Se asume que `layout` tiene el método `addWidget`.
            - Se asume que `self.parent.visor` tiene los métodos:
                `mostrarHistograma`, `setZoomCombo` y `reiniciarImagen`.
        """
        
        if hasattr(layout, 'addWidget') and hasattr(self.parent, 'visor'):
        
            # -------------------------------------------------
            # se agrega un separador visual
            # -------------------------------------------------
            layout.addWidget(self.configurarSeparador())
        
            # -------------------------------------------------
            # Botón "Mostrar Histograma"
            # -------------------------------------------------
            layout.addWidget(QLabel("Histograma de la imagen actual"))
            btn_histograma = QPushButton("Mostrar")
            btn_histograma.clicked.connect(self.parent.visor.mostrarHistograma)
            layout.addWidget(btn_histograma)
            
            # -------------------------------------------------
            # se agrega un separador visual
            # -------------------------------------------------
            layout.addWidget(self.configurarSeparador())
    
            # -------------------------------------------------
            # zoom
            # -------------------------------------------------
            layout.addWidget(QLabel("Zoom de Imagen"))

            self.combo_zoom = QComboBox()
            # Lista de opciones: de 50% a 150% (ajusta el rango si lo deseas)
            zoom_values = [f"{i}%" for i in range(100, 301, 10)]
            self.combo_zoom.addItems(zoom_values)
            self.combo_zoom.setCurrentText("100%")  # Tamaño normal

            # Conectar la selección para aplicar el zoom
            self.combo_zoom.currentIndexChanged.connect(
                lambda: self.parent.visor.setZoomCombo(self.combo_zoom.currentText())
            )

            layout.addWidget(self.combo_zoom)
            
            # -------------------------------------------------
            # se agrega un separador visual
            # -------------------------------------------------
            layout.addWidget(self.configurarSeparador())
                                    
            # -------------------------------------------------
            # Botón "Fusionar Imagenes"
            # -------------------------------------------------                         
            layout.addWidget(QLabel("Fusionar con otra imagen"))                        
            
            # Barra para mostrar la ruta de la segunda imagen
            layout_ruta2 = QHBoxLayout()
            etiqueta_ruta2 = QLabel("Ruta:")
            self.barraRutaImg2 = QLineEdit()
            self.barraRutaImg2.setReadOnly(True)
            layout_ruta2.addWidget(etiqueta_ruta2)
            layout_ruta2.addWidget(self.barraRutaImg2)
            layout.addLayout(layout_ruta2)
            
            # Botón para cargar la segunda imagen
            btn_cargar_imagen2 = QPushButton("Seleccionar imagen")
            btn_cargar_imagen2.clicked.connect(self.seleccionarImagenSecundaria)
            layout.addWidget(btn_cargar_imagen2)
            
            # Slider para la transparencia (alpha)
            layout.addWidget(QLabel("Transparencia"))
            self.slider_alpha = QSlider(Qt.Orientation.Horizontal)
            self.slider_alpha.setMinimum(0)
            self.slider_alpha.setMaximum(100)
            self.slider_alpha.setValue(50)  # 50% transparencia por defecto
            self.slider_alpha.setTickInterval(10)
            self.slider_alpha.setSingleStep(1)
            # Conectar el cambio de valor para aplicar en tiempo real
            self.slider_alpha.valueChanged.connect(self.aplicarFusionImagenes)
            layout.addWidget(self.slider_alpha)
            
            # Slider para posición X
            layout.addWidget(QLabel("Posición X"))
            self.slider_x_offset = QSlider(Qt.Orientation.Horizontal)
            self.slider_x_offset.setMinimum(0)
            self.slider_x_offset.setMaximum(100)
            self.slider_x_offset.setValue(0)
            self.slider_x_offset.setTickInterval(10)
            self.slider_x_offset.setSingleStep(1)
            # Conectar el cambio de valor para aplicar en tiempo real
            self.slider_x_offset.valueChanged.connect(self.aplicarFusionImagenes)
            layout.addWidget(self.slider_x_offset)
            
            # Slider para posición Y
            layout.addWidget(QLabel("Posición Y"))
            self.slider_y_offset = QSlider(Qt.Orientation.Horizontal)
            self.slider_y_offset.setMinimum(0)
            self.slider_y_offset.setMaximum(100)
            self.slider_y_offset.setValue(0)
            self.slider_y_offset.setTickInterval(10)
            self.slider_y_offset.setSingleStep(1)
            # Conectar el cambio de valor para aplicar en tiempo real
            self.slider_y_offset.valueChanged.connect(self.aplicarFusionImagenes)
            layout.addWidget(self.slider_y_offset)
            
            # Separador para los nuevos botones
            layout.addWidget(self.configurarSeparador())
            
            # Slider para ajustar el tamaño de la imagen secundaria
            layout.addWidget(QLabel("Tamaño imagen secundaria"))
            self.slider_tamano = QSlider(Qt.Orientation.Horizontal)
            self.slider_tamano.setMinimum(10)  # 10% del tamaño original
            self.slider_tamano.setMaximum(200) # 200% del tamaño original
            self.slider_tamano.setValue(100)   # 100% = tamaño original
            self.slider_tamano.setTickInterval(10)
            self.slider_tamano.setSingleStep(5)
            # Conectar el cambio de valor para aplicar en tiempo real
            self.slider_tamano.valueChanged.connect(self.ajustarTamanoImagenSecundaria)
            layout.addWidget(self.slider_tamano)
            
            # Botón para descartar los cambios de fusión
            btn_descartar_fusion = QPushButton("Descartar cambios")
            btn_descartar_fusion.clicked.connect(self.descartarCambiosFusion)
            layout.addWidget(btn_descartar_fusion)
            
            # -------------------------------------------------
            # se agrega un separador visual
            # -------------------------------------------------
            layout.addWidget(self.configurarSeparador())
                        
            # -------------------------------------------------
            # Botón "Deshacer Modificaciones"
            # -------------------------------------------------     
            layout.addWidget(QLabel("Reiniciar imagen"))       
            btn_reiniciar = QPushButton("Borrar modificaciones")
            btn_reiniciar.clicked.connect(self.parent.visor.reiniciarImagen)
            layout.addWidget(btn_reiniciar)
    
    def cambiarValorSlider(self, valor):
        """
        Cambia el valor del slider a un valor normalizado.
        Este método toma un valor entero proporcionado por el slider, 
        lo divide entre 100 y devuelve el valor resultante como un 
        número flotante normalizado.
        Args:
            valor (int): El valor actual del slider, esperado en el rango de 0 a 100.
        Returns:
            float: El valor normalizado del slider, en el rango de 0.0 a 1.0.
        """
        
        valor_normalizado = valor / 100.0
        return valor_normalizado
    
    def aplicarFiltroZonas(self):
        """
        Aplica un filtro de zonas en el visor basado en los parámetros seleccionados.
        Este método obtiene los valores seleccionados de los controles de la interfaz 
        (umbral, modo y color) y los utiliza para aplicar un filtro en el visor.
        Parámetros:
        - No recibe parámetros directamente, utiliza los valores seleccionados en los 
          controles de la interfaz gráfica.
        Detalles:
        - El umbral se normaliza a un rango de 0.0 a 1.0.
        - El modo del filtro se obtiene del texto seleccionado en el combo box correspondiente.
        - El color se mapea a un valor RGB normalizado basado en el texto seleccionado 
          en el combo box de colores.
        Llama a:
        - `self.parent.visor.aplicarFiltroZonas(umbral, modo, color)`: Método del visor 
          que realiza la aplicación del filtro con los parámetros calculados.
        """
        
        # Obtener los valores seleccionados
        umbral = self.slider_umbral.value() / 100.0  # Normalizamos (0.0 - 1.0)
        modo = self.combo_modoFiltro.currentText()
        
        # Mapeo de nombre de color a valor RGB (normalizado)
        colores = {
            "Rojo": [1, 0, 0],
            "Verde": [0, 1, 0],
            "Azul": [0, 0, 1]
        }
        color = colores.get(self.combo_colorFiltro.currentText(), [1, 0, 0])
        
        # Llama al método del visor para aplicar el filtro
        self.parent.visor.aplicarFiltroZonas(umbral, modo, color)
        
        
    # -------------------------------------------------
    # Funciones para la opción de Fusionar Imagenes
    # -------------------------------------------------     
    def aplicarFusionImagenes(self):
        """
        Aplica la fusión de la imagen actual con la imagen secundaria.
        
        Este método obtiene los valores seleccionados de los sliders de transparencia,
        posición X y posición Y, y los utiliza para aplicar la fusión de imágenes.
        
        Es llamado tanto por el botón "Aplicar fusión" como automáticamente cuando
        se ajustan los sliders de transparencia o posición.
        """
        try:
            # Intentamos acceder directamente a la imagen secundaria
            imagen_secundaria = self.parent.visor.imagen_secundaria
            
            # Si imagen_secundaria es None, salimos de la función
            if imagen_secundaria is None:
                return
                
            # Obtener los valores de los sliders
            alpha = self.slider_alpha.value() / 100.0  # Normalizar entre 0 y 1
            
            # Obtener dimensiones de la imagen principal para calcular desplazamientos relativos
            h, w = self.parent.visor.imagen.shape[:2]
            x_offset = int((self.slider_x_offset.value() / 100.0) * w)
            y_offset = int((self.slider_y_offset.value() / 100.0) * h)
            
            # Llamar al método del visor para aplicar la fusión
            self.parent.visor.aplicarFusionImagenes(imagen_secundaria, alpha, x_offset, y_offset)
            
        except Exception as e:
            # Si hay algún error (imagen no cargada, etc.), simplemente continuamos sin aplicar la fusión
            pass
            
    
    def seleccionarImagenSecundaria(self):
        """
        Abre un diálogo para seleccionar una imagen secundaria y la carga.
        
        Este método muestra un diálogo de selección de archivos y permite al usuario
        elegir una imagen secundaria para fusionar con la imagen principal.
        """
        from PyQt6.QtWidgets import QFileDialog
        
        options = QFileDialog.Option.ReadOnly
        filePath, _ = QFileDialog.getOpenFileName(
            self.parent,
            "Seleccionar Imagen Secundaria",
            "",
            "Imágenes (*.png *.jpg *.bmp *.jpeg);;Todos los archivos (*)",
            options=options
        )
        
        if filePath:
            # Cargar la imagen secundaria en el visor
            self.parent.visor.cargarImagenSecundaria(filePath)
            # Actualizar la ruta en la interfaz
            self.barraRutaImg2.setText(filePath)
     
    def ajustarTamanoImagenSecundaria(self):
        """
        Ajusta el tamaño de la imagen secundaria basado en el valor del slider.
        
        Este método toma el valor actual del slider de tamaño, lo convierte a un
        factor de escala (porcentaje/100) y llama al método del visor para 
        redimensionar la imagen secundaria y aplicar la fusión en tiempo real.
        """
        try:
            # Verificar que existe una imagen secundaria
            if self.parent.visor.imagen_secundaria is None:                
                return
                
            # Convertir el valor del slider a un factor de escala
            factor = self.slider_tamano.value() / 100.0
            
            # Redimensionar la imagen secundaria
            self.parent.visor.redimensionarImagenSecundaria(factor)
            
            # Aplicar la fusión con la nueva imagen redimensionada
            self.aplicarFusionImagenes()
            
        except Exception as e:
            print(f"Error al ajustar tamaño: {e}")
    
    def descartarCambiosFusion(self):
        """
        Descarta completamente todos los cambios de fusión y reinicia el estado de la fusión.
        
        Este método realiza las siguientes acciones:
        1. Restaura la imagen mostrada a su estado base (sin la fusión)
        2. Elimina la imagen secundaria
        3. Reinicia los controles de fusión a sus valores predeterminados
        4. Limpia la ruta de la imagen secundaria en la interfaz
        """
        try:
            # Verificar que existe una imagen base
            if self.parent.visor.imagen_base is not None:
                # Restaurar la imagen base sin aplicar fusión
                self.parent.visor.restaurarImagenBase()
                
                # Eliminar la imagen secundaria y su referencia original
                if hasattr(self.parent.visor, 'imagen_secundaria'):
                    self.parent.visor.imagen_secundaria = None
                    
                if hasattr(self.parent.visor, 'imagen_secundaria_original'):
                    self.parent.visor.imagen_secundaria_original = None
                
                # Limpiar la ruta de la imagen secundaria
                self.parent.visor.ruta_imagen_secundaria = ""
                self.barraRutaImg2.setText("")
                
                # Reiniciar los valores de los sliders a sus valores predeterminados
                self.slider_alpha.setValue(50)
                self.slider_x_offset.setValue(0)
                self.slider_y_offset.setValue(0)
                self.slider_tamano.setValue(100)
                                
        except Exception as e:
            print(f"Error al descartar cambios: {e}")
     
     