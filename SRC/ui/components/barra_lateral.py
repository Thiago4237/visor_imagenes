from PyQt6.QtWidgets import QToolBar,  QDockWidget, QWidget, QLabel, QVBoxLayout
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

        parent.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_widget)

        # Botones de acción
        self.initActions()

    def initActions(self):
        ajustes_basicos_icon_path = cfg.ICONOS["ajustesBasicos"]
        ajustes_basicos_action = QAction(QIcon(ajustes_basicos_icon_path), "Ajustes Básicos", self)
        ajustes_basicos_action.setCheckable(True) 
        ajustes_basicos_action.triggered.connect(lambda: self.mostrarOpciones("Básicos"))
        self.addAction(ajustes_basicos_action)

        ajustes_filtros_icon_path = cfg.ICONOS["ajustesDeFiltros"]
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

        # Crear el nuevo widget con las opciones
        widget_opciones = QWidget()
        layout = QVBoxLayout(widget_opciones)
        
        label = QLabel(f"Ajustes {tipo}")
        layout.addWidget(label)

        self.dock_widget.setWidget(widget_opciones)
        self.dock_widget.setWindowTitle(f"Ajustes {tipo}")  # Guardar el título para verificar estado
        self.dock_widget.setVisible(True)  # Mostrar el dock widget

