# Visor de Imágenes

Este visor de imágenes es una aplicación desarrollada en Python utilizando **PyQt6** que permite visualizar, manipular y editar imágenes de manera eficiente.

![Visor GIF](Resources/visor_imagen/visor_imagen.gif)

## **Características Principales**
- **Visualización optimizada**: Escala automáticamente imágenes grandes (>1M píxeles) para mantener un rendimiento fluido.
- **Historial de cambios**: Sistema de deshacer/rehacer para todas las modificaciones.
- **Manipulación de imágenes**:
  - Ajustes de **brillo** y **contraste**.
  - **Rotación** de imágenes.
  - **Fusión** de imágenes secundarias.
  - **Zoom inteligente** centrado en el cursor.
- **Interfaz intuitiva**: Controles sencillos y barra de ruta para navegación.

---

## **Instalación**

### **Requisitos**
- Python 3.8 o superior.
- Un entorno virtual (opcional, pero recomendado).

### **Para instalar las dependencias**
   ```bash
   pip install -r install.txt
   ```

---

## **Atajos y Gestos**

### **Atajos de Teclado**
- **Ctrl+L**: Cargar imagen.
- **Ctrl+G**: Guardar imagen.
- **Ctrl+A**: Actualizar imagen.
- **Ctrl+Z**: Deshacer último cambio.
- **Ctrl+Y**: Rehacer cambio.
- **1**: Abrir ajustes básicos.
- **2**: Abrir ajustes de filtros.
- **3**: Abrir ajustes avanzados.

### **Gestos con Ratón**
- **Rueda del ratón**: Zoom in/out centrado en la posición del cursor.
- **Arrastrar**: Navegar por la imagen cuando está ampliada.

### **Gestos Táctiles**
- **Pellizcar (Pinch)**: Zoom in/out en dispositivos táctiles.