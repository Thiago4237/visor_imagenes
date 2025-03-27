from PyQt6.QtWidgets import QToolBar, QPushButton, QDockWidget, QWidget, QLabel, QVBoxLayout, QSlider
from PyQt6.QtGui import QIcon, QAction
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

        # Botones de acción
        self.initActions()

    def initActions(self):
        ajustes_basicos_icon_path = cfg.ICONOS["ajustesBasicos"]
        ajustes_basicos_action = QAction(QIcon(ajustes_basicos_icon_path), "Ajustes Básicos", self)
        ajustes_basicos_action.setCheckable(True) 
        ajustes_basicos_action.triggered.connect(lambda: self.mostrarOpciones("Básicos"))
        self.addAction(ajustes_basicos_action)

        ajustes_filtros_icon_path = cfg.ICONOS["guardar"]
        ajustes_filtros_action = QAction(QIcon(ajustes_filtros_icon_path), "Ajustes de Filtros", self)
        ajustes_basicos_action.setCheckable(True) 
        ajustes_filtros_action.triggered.connect(lambda: self.mostrarOpciones("de Filtros"))
        self.addAction(ajustes_filtros_action)

        ajustes_avanzados_icon_path = cfg.ICONOS["ajustesAvanzados"]
        ajustes_avanzados_action = QAction(QIcon(ajustes_avanzados_icon_path), "Ajustes Avanzados", self)
        ajustes_avanzados_action.setCheckable(True) 
        ajustes_avanzados_action.triggered.connect(lambda: self.mostrarOpciones("Avanzados"))
        self.addAction(ajustes_avanzados_action)

    def mostrarOpciones(self, tipo):
        """Muestra u oculta el panel lateral con las opciones correspondientes."""
        if self.dock_widget.isVisible() and self.dock_widget.windowTitle() == f"Ajustes {tipo}":
            self.dock_widget.setVisible(False)  # Ocultar si ya está abierto con la misma opción
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
        
        # label = QLabel(f"Ajustes {tipo}")
        # layout.addWidget(label)

        if tipo == "Básicos":
            
            # Botón "Invertir colores"
            btn_invertir_color = QPushButton("Invertir colores")
            btn_invertir_color.clicked.connect(self.parent.visor.invertirColoresImagen)
            layout.addWidget(btn_invertir_color)
            
             # Botón "binarizar"
            btn_binarizar = QPushButton("Binarizar")
            btn_binarizar.clicked.connect(self.parent.visor.binarizarImagen)
            layout.addWidget(btn_binarizar)
            
            # **Slider de Brillo (0 a 2)**
            self.slider_brillo = QSlider(Qt.Orientation.Horizontal)
            self.slider_brillo.setMinimum(1)
            self.slider_brillo.setMaximum(200)  # Rango: 0.0 a 2.0 (100 = 1.0)
            self.slider_brillo.setValue(100)  # Valor inicial (1.0)
            self.slider_brillo.setTickInterval(10)
            self.slider_brillo.setSingleStep(1)
            self.slider_brillo.valueChanged.connect(lambda val: self.parent.visor.aplicarAjusteBrillo(self.cambiarValorSlider(val)))


            layout.addWidget(QLabel("Ajuste de Brillo"))
            layout.addWidget(self.slider_brillo)
            
            # 🔹 Slider para contraste (-1.0 a 1.0 con neutro en 0.0)
            self.sliderContraste = QSlider(Qt.Orientation.Horizontal)
            self.sliderContraste.setMinimum(1)   # Equivalente a 0.01
            self.sliderContraste.setMaximum(200)  # Equivalente a 2.0
            self.sliderContraste.setValue(100)    # Neutro = 1.0
            self.sliderContraste.setSingleStep(1)
            self.sliderContraste.valueChanged.connect(lambda val: self.parent.visor.ajustarContraste(self.cambiarValorSlider(val)))


            layout.addWidget(QLabel("Contraste"))
            layout.addWidget(self.sliderContraste)
            
            self.slider_rotacion = QSlider(Qt.Orientation.Horizontal)
            self.slider_rotacion.setMinimum(-180)  # Rotación mínima -180°
            self.slider_rotacion.setMaximum(180)   # Rotación máxima 180°
            self.slider_rotacion.setValue(0)       # Rotación inicial 0°
            self.slider_rotacion.setTickInterval(10)
            self.slider_rotacion.setSingleStep(1)

            # Conectar el slider para aplicar la rotación en tiempo real
            self.slider_rotacion.valueChanged.connect(lambda val: self.parent.visor.aplicarRotacion(val))

            layout.addWidget(QLabel("Rotación de Imagen"))
            layout.addWidget(self.slider_rotacion)
            

        widget_opciones.setLayout(layout)

        # Establecer el nuevo widget en el dock
        self.dock_widget.setWidget(widget_opciones)
        self.dock_widget.setWindowTitle(f"Ajustes {tipo}")  # Guardar el título para verificar estado
        self.dock_widget.setVisible(True)  # Mostrar el dock widget
        

    def cambiarValorSlider(self, valor):
        """Convierte el valor de 0-100 a 0-1 y lo retorna"""
        valor_normalizado = valor / 100.0
        return valor_normalizado
        