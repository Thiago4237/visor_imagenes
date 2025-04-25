import os
from PyQt6.QtWidgets import QToolBar, QLabel, QWidget, QSizePolicy, QFileDialog
from PyQt6.QtGui import QIcon, QPixmap, QAction
from PyQt6.QtCore import QSize
import config.config as cfg

class BarraSuperior(QToolBar):
    def __init__(self, parent):
        """
        Inicializa una instancia de la clase BarraSuperior.
        Args:
            parent (QMainWindow): Referencia al widget principal (QMainWindow) que actúa como padre.
        Atributos:
            parent_widget (QMainWindow): Guarda la referencia al QMainWindow principal.
        Acciones:
            - Configura el tamaño de los íconos en 32x32 píxeles.
            - Agrega el logo a la izquierda de la barra.
            - Añade espaciadores flexibles para controlar la disposición de los botones.
            - Inicializa los botones de acción llamando al método `initActionsTop`.
        """
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
        
        # Añadir espacio flexible para empujar los botones
        spacer_left = QWidget()
        spacer_left.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.addWidget(spacer_left)

        # Botones de acción
        self.initActionsTop()
    
    def initActionsTop(self):
        """
        Inicializa y agrega los botones a la barra de herramientas superior.
        Este método configura los botones principales en la barra superior: "Cargar", 
        "Guardar", "Actualizar", "Deshacer" y "Rehacer". Cada botón tiene un ícono, 
        un texto descriptivo y está asociado a una acción específica.
        Acciones configuradas:
            - "Cargar": Permite al usuario cargar una imagen desde el sistema de archivos.
            - "Guardar": Permite al usuario guardar la imagen actual en el sistema de archivos.
            - "Actualizar": Actualiza la imagen mostrada en el visor.
            - "Deshacer": Deshace la última modificación realizada en la imagen.
            - "Rehacer": Rehace la última modificación deshecha en la imagen.
        Notas:
            - Los íconos de las acciones se obtienen de la configuración `cfg.ICONOS`.
            - Algunas acciones tienen atajos de teclado definidos en `cfg.ATAJOS`.
            - Cada acción está conectada a su correspondiente método de callback en esta clase.
        """
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
        deshacer_action.setShortcut(cfg.ATAJOS["deshacer"])
        self.addAction(deshacer_action)

        # Botón de Rehacer
        rehacer_action = self.createAction("rehacer", "Rehacer", self.rehacerCambios)
        rehacer_action.setShortcut(cfg.ATAJOS["rehacer"])
        self.addAction(rehacer_action)

        
    def createAction(self, icono_nombre, texto, callback):
        """
        Crea un botón de acción con su respectivo icono, texto y función asociada.
        Args:
            icono_nombre (str): Nombre de la clave en el diccionario cfg.ICONOS para obtener la ruta del ícono.
            texto (str): Texto descriptivo que se mostrará como tooltip del botón.
            callback (function): Función que se ejecutará cuando se active el botón.
        Returns:
            QAction: Un objeto QAction configurado con el ícono, texto y callback especificados.
        Notas:
            - El ícono se obtiene del diccionario cfg.ICONOS usando el nombre proporcionado.
            - La acción se configura como "checkable" para permitir un estado activo/inactivo.
            - La acción se conecta a la función callback proporcionada para responder a los clics.
        """
        icono_path = cfg.ICONOS[icono_nombre]
        action = QAction(QIcon(icono_path), texto, self.parent_widget)
        action.setCheckable(True)
        action.triggered.connect(callback)
        return action

    def cargarImagen(self):
        """
        Abre un cuadro de diálogo para seleccionar y cargar una imagen en el visor.
        Este método presenta al usuario un cuadro de diálogo estándar de selección de archivos,
        filtrado para mostrar solo archivos de imagen (PNG, JPG, BMP). Si el usuario selecciona
        un archivo válido, la imagen se carga en el visor de la aplicación.
        Acciones:
            - Muestra un cuadro de diálogo para seleccionar un archivo de imagen.
            - Si se selecciona un archivo, lo carga en el visor de imágenes.
            - Llama al método desmarcarBoton para desactivar el estado del botón después de la acción.
        Notas:
            - Utiliza QFileDialog.getOpenFileName para mostrar el diálogo de selección.
            - Llama al método cargarImagen del visor (self.parent_widget.visor) para procesar la imagen.
            - Solo actúa si el usuario selecciona un archivo (filePath no está vacío).
        """
        filePath, _ = QFileDialog.getOpenFileName(self.parent_widget, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.bmp)")
        if filePath:
            self.parent_widget.visor.cargarImagen(filePath)
        self.desmarcarBoton()

    def guardarImagen(self):
        """
        Abre un cuadro de diálogo para guardar la imagen actual del visor en un archivo.
        Este método presenta al usuario un cuadro de diálogo estándar de guardado de archivos,
        permitiendo guardar la imagen actual en formato PNG, JPG o BMP. Si el usuario especifica
        una ubicación y nombre de archivo válidos, la imagen se guarda en el sistema de archivos.
        Acciones:
            - Muestra un cuadro de diálogo para especificar la ubicación y nombre del archivo.
            - Si se proporciona una ruta válida, guarda la imagen actual en esa ubicación.
            - Llama al método desmarcarBoton para desactivar el estado del botón después de la acción.
        Notas:
            - Utiliza QFileDialog.getSaveFileName para mostrar el diálogo de guardado.
            - Llama al método guardarImagen del visor (self.parent_widget.visor) para realizar el guardado.
            - Solo actúa si el usuario proporciona una ruta válida (filePath no está vacío).
        """
        filePath, _ = QFileDialog.getSaveFileName(self.parent_widget, "Guardar imagen", "", "Imágenes (*.png *.jpg *.bmp)")
        if filePath:
            self.parent_widget.visor.guardarImagen(filePath)
        self.desmarcarBoton()

    def actualizarImagen(self):
        """
        Llama a la función de actualizar imagen en el visor.
        Este método actúa como un puente para invocar la función actualizarImagen
        del componente visor asociado al widget padre. Una vez completada la
        actualización, desmarca el botón que activó esta acción.
        Acciones:
            - Llama al método actualizarImagen del visor para refrescar la imagen mostrada.
            - Llama al método desmarcarBoton para desactivar el estado del botón después de la acción.
        Notas:
            - Se asume que self.parent_widget.visor tiene implementado un método actualizarImagen.
        """
        self.parent_widget.visor.actualizarImagen()
        self.desmarcarBoton()

    def deshacerCambios(self):
        """
        Llama a la función de deshacer en el visor de imágenes.
        Este método actúa como un puente para invocar la función deshacerCambios
        del componente visor asociado al widget padre. Permite revertir la última
        modificación realizada en la imagen. Una vez completada la operación,
        desmarca el botón que activó esta acción.
        Acciones:
            - Llama al método deshacerCambios del visor para revertir la última operación.
            - Llama al método desmarcarBoton para desactivar el estado del botón después de la acción.
        Notas:
            - Se asume que self.parent_widget.visor tiene implementado un método deshacerCambios.
        """
        self.parent_widget.visor.deshacerCambios()
        self.desmarcarBoton()

    def rehacerCambios(self):
        """
        Llama a la función de rehacer en el visor de imágenes.
        Este método actúa como un puente para invocar la función rehacerCambios
        del componente visor asociado al widget padre. Permite restaurar la última
        modificación deshecha en la imagen. Una vez completada la operación,
        desmarca el botón que activó esta acción.
        Acciones:
            - Llama al método rehacerCambios del visor para restaurar la última operación deshecha.
            - Llama al método desmarcarBoton para desactivar el estado del botón después de la acción.
        Notas:
            - Se asume que self.parent_widget.visor tiene implementado un método rehacerCambios.
        """
        self.parent_widget.visor.rehacerCambios()
        self.desmarcarBoton()

    def desmarcarBoton(self):
        """
        Desmarca el botón después de hacer clic.
        Este método identifica el objeto que envió la señal (sender) y, si es un QAction
        que está configurado como "checkable", lo desmarca estableciendo su propiedad
        checked a False. Esto asegura que los botones de la barra de herramientas
        vuelvan a su estado visual normal después de ser presionados.
        Acciones:
            - Identifica el objeto que envió la señal.
            - Si el objeto es un QAction y está configurado como "checkable", lo desmarca.
        Notas:
            - Este método es útil para botones que no mantienen un estado activado
              pero que se configuran como "checkable" para efectos visuales.
        """
        sender = self.sender()
        if isinstance(sender, QAction) and sender.isCheckable():
            sender.setChecked(False)
