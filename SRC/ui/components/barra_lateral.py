from PyQt6.QtWidgets import ( QToolBar, QComboBox, QDial, QPushButton, QDockWidget, 
                             QWidget, QLabel, QVBoxLayout, QSlider)
from PyQt6.QtGui import QIcon, QAction, QActionGroup
from PyQt6.QtCore import QSize, Qt
import config.config as cfg

class BarraLateral(QToolBar):
    def __init__(self, parent):
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
        # self.dock_widget.visibilityChanged.connect(self.refrescarVisor) # Conectar la señal de visibilidad al método refrescarVisor                

        # Botones de acción
        self.initActions()

    # def refrescarVisor(self):
    #         """Forza la actualización del visor cuando la barra lateral se oculta/muestra."""
    #         if hasattr(self.parent, 'visor'):
    #             self.parent.visor.update()  # Forzar repintado del visor

    def initActions(self):
        action_group = QActionGroup(self)  # Crear un grupo para las acciones
        action_group.setExclusive(True)  # Solo una acción puede estar activada a la vez

        ajustes_basicos_icon_path = cfg.ICONOS["ajustesBasicos"]
        ajustes_basicos_action = QAction(QIcon(ajustes_basicos_icon_path), "Ajustes Básicos", self)
        ajustes_basicos_action.setCheckable(True)  
        ajustes_basicos_action.triggered.connect(lambda: self.mostrarOpciones("Básicos"))
        self.addAction(ajustes_basicos_action)
        action_group.addAction(ajustes_basicos_action) 

        ajustes_filtros_icon_path = cfg.ICONOS["ajustesDeFiltros"]
        ajustes_filtros_action = QAction(QIcon(ajustes_filtros_icon_path), "Ajustes de Filtros", self)
        ajustes_filtros_action.setCheckable(True)  
        ajustes_filtros_action.triggered.connect(lambda: self.mostrarOpciones("de Filtros"))
        self.addAction(ajustes_filtros_action)
        action_group.addAction(ajustes_filtros_action)  

        ajustes_avanzados_icon_path = cfg.ICONOS["ajustesAvanzados"]
        ajustes_avanzados_action = QAction(QIcon(ajustes_avanzados_icon_path), "Ajustes Avanzados", self)
        ajustes_avanzados_action.setCheckable(True)  
        ajustes_avanzados_action.triggered.connect(lambda: self.mostrarOpciones("Avanzados"))
        self.addAction(ajustes_avanzados_action)
        action_group.addAction(ajustes_avanzados_action) 


    def mostrarOpciones(self, tipo):
        """Muestra u oculta el panel lateral con las opciones correspondientes."""
        sender_action = self.sender()  # Obtener la acción que activó la señal

        if self.dock_widget.isVisible() and self.dock_widget.windowTitle() == f"Ajustes {tipo}":
            self.dock_widget.setVisible(False)  # Ocultar si ya está abierto con la misma opción
            if sender_action:
                sender_action.setChecked(False)  # Desmarcar el botón
            return

        # Limpiar cualquier widget previo en el dock
        for i in reversed(range(self.layoutOpciones.count())):
            widget_to_remove = self.layoutOpciones.itemAt(i).widget()
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

        # -------------------------------------------------
        # Botón "Invertir colores"
        # -------------------------------------------------
        btn_reiniciar = QPushButton("deshacer modificaciones")
        btn_reiniciar.clicked.connect(self.parent.visor.reiniciarImagen)
        layout.addWidget(btn_reiniciar)

        if tipo == "Básicos":
            
            # -------------------------------------------------
            # **Slider de Brillo (0 a 2)**
            # -------------------------------------------------
            self.slider_brillo = QSlider(Qt.Orientation.Horizontal)
            self.slider_brillo.setMinimum(1)
            self.slider_brillo.setMaximum(200)  # Rango: 0.0 a 2.0 (100 = 1.0)
            self.slider_brillo.setValue(100)  # Valor inicial (1.0)
            self.slider_brillo.setTickInterval(10)
            self.slider_brillo.setSingleStep(1)
            self.slider_brillo.valueChanged.connect(lambda val: self.parent.visor.aplicarAjusteBrillo(self.cambiarValorSlider(val)))

            layout.addWidget(QLabel("Ajuste de Brillo"))
            layout.addWidget(self.slider_brillo)
            
            # -------------------------------------------------
            # 🔹 Slider para contraste negativo
            # -------------------------------------------------
            self.sliderContraste = QSlider(Qt.Orientation.Horizontal)
            self.sliderContraste.setMinimum(1)   # Equivalente a 0.01
            self.sliderContraste.setMaximum(100)  # Equivalente a 1.0
            self.sliderContraste.setValue(1)    # Neutro = 0.01
            self.sliderContraste.setSingleStep(1)
            self.sliderContraste.valueChanged.connect(lambda val: self.parent.visor.ajustarContrasteNegativo(self.cambiarValorSlider(val)))

            layout.addWidget(QLabel("Contraste negativo"))
            layout.addWidget(self.sliderContraste)
            
            # -------------------------------------------------
            # 🔹 Slider para contraste positivo
            # -------------------------------------------------
            self.sliderContraste = QSlider(Qt.Orientation.Horizontal)
            self.sliderContraste.setMinimum(1)   # Equivalente a 0.01
            self.sliderContraste.setMaximum(100)  # Equivalente a 1.0
            self.sliderContraste.setValue(100)    # Neutro = 1.0
            self.sliderContraste.setSingleStep(1)
            self.sliderContraste.valueChanged.connect(lambda val: self.parent.visor.ajustarContrastePositivo(self.cambiarValorSlider(val)))

            layout.addWidget(QLabel("Contraste positivo"))
            layout.addWidget(self.sliderContraste)

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
        
        if tipo == "de Filtros" :
            
            # -------------------------------------------------
            # Botón "Invertir colores"
            # -------------------------------------------------
            layout.addWidget(QLabel("Invertir Colores"))
            btn_invertir_color = QPushButton("Invertir")
            btn_invertir_color.clicked.connect(self.parent.visor.invertirColoresImagen)
            layout.addWidget(btn_invertir_color)

            # -------------------------------------------------
            # Botón "Invertir colores"
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
                self.parent.visor.aplicarCapaImagen(indice_capa)
                
            # Función para aplicar la selección de capa
            def aplicarCapaSeleccionada():
                nombre_capa = self.combo_capa.currentText()
                indice_capa = capas[nombre_capa]
                if indice_capa == -1:
                    self.parent.visor.reiniciarImagen()
                else:
                    self.parent.visor.aplicarCapaImagen(indice_capa)

            # Conectar el evento de selección
            self.combo_capa.currentIndexChanged.connect(aplicarCapaSeleccionada)

            # Agregar al layout
            layout.addWidget(self.combo_capa)

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
                    self.parent.visor.reiniciarImagen()
                else:
                    self.parent.visor.aplicarQuitarCanal(indice_canal)

            # Conectar el evento de selección
            self.combo_eliminar_canal.currentIndexChanged.connect(aplicarQuitarCanal)

            # Agregar al layout
            layout.addWidget(self.combo_eliminar_canal)


        if tipo == 'Avanzados':
            
            # -------------------------------------------------
            # Botón "binarizar"
            # -------------------------------------------------
            btn_binarizar = QPushButton("Binarizar")
            btn_binarizar.clicked.connect(self.parent.visor.binarizarImagen)
            layout.addWidget(btn_binarizar)

        widget_opciones.setLayout(layout)

        # Establecer el nuevo widget en el dock
        self.dock_widget.setWidget(widget_opciones)
        self.dock_widget.setWindowTitle(f"Ajustes {tipo}")  # Guardar el título para verificar estado
        self.dock_widget.setVisible(True)  # Mostrar el dock widget
        

    def cambiarValorSlider(self, valor):
        """Convierte el valor de 0-100 a 0-1 y lo retorna"""
        valor_normalizado = valor / 100.0
        return valor_normalizado
        