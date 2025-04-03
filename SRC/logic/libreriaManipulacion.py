import numpy as np
import matplotlib.pyplot as plt
import cv2

# cargar imagen
def cargar_imagen(ruta):
    """
    Carga una imagen usando matplotlib y la convierte en un array de numpy.
    
    Parámetros:
    - ruta: Ruta de la imagen a cargar.

    Retorna:
    - Imagen como array de numpy (formato RGB normalizado 0-1 si es float).
    """
    img = plt.imread(ruta)
    if img.dtype == np.uint8:  # Si la imagen está en 0-255, normalizar a 0-1
        img = img / 255.0
    return img

# eliminar capa alpha
def eliminarCapaAlpha(imagen):
    """
    Elimina el canal Alpha de una imagen si está presente.
    Esta función verifica si la imagen tiene 4 canales (RGBA). 
    Si es así, elimina el cuarto canal (Alpha) y devuelve la imagen 
    con solo los canales RGB.
    Parámetros:
    imagen (numpy.ndarray): Una matriz que representa la imagen. 
                             Se espera que tenga una forma de 3 dimensiones 
                             donde la última dimensión indica los canales de color.
    Retorna:
    numpy.ndarray: La imagen sin el canal Alpha (solo canales RGB) si tenía 4 canales, 
                   o la imagen original si no tenía un canal Alpha.
    """
    
    if imagen.shape[-1] == 4:  # Si tiene 4 canales (RGBA)
        imagen = imagen[:, :, :3]  # Eliminar el canal Alpha
    return imagen

# ajuste de brillo 
def ajusteBrillo (imagen, brillo):
    """
    Ajusta el brillo de una imagen.
    Parámetros:
    imagen (numpy.ndarray): La imagen a la que se le ajustará el brillo.
    brillo (int o float): El valor del brillo a ajustar. Puede ser positivo para aumentar el brillo o negativo para disminuirlo.
    Retorna:
    numpy.ndarray: La imagen con el brillo ajustado.
    """
    return np.clip(imagen * brillo, 0, 1)

# ajuste de canal R-G-B (0-1-2)
def ajusteCanal(imagen, ajuste, capa):
    """
    Ajusta el valor de un canal específico de una imagen.
    Parámetros:
    imagen (numpy.ndarray): La imagen a ajustar, representada como un arreglo numpy.
    ajuste (int o float): El valor de ajuste que se sumará al canal especificado.
    capa (int): El índice del canal a ajustar (0 para rojo, 1 para verde, 2 para azul en una imagen RGB).
    Retorna:
    numpy.ndarray: La imagen ajustada con el valor del canal especificado modificado.
    """
    img_canal = np.copy(imagen)
    img_canal[:,:,capa] = np.clip(img_canal[:,:,capa] + ajuste, 0, 1)
    return img_canal

# ajuste de contraste tipo = 0 -> oscuras, tipo = 1 -> claras
def ajusteContraste(imagen, contraste, tipo):
    """
    Ajusta el contraste de una imagen utilizando diferentes métodos.
    Parámetros:
    imagen (numpy.ndarray): La imagen de entrada en formato de matriz numpy.
    contraste (float): El valor del contraste a aplicar.
    tipo (int): El tipo de ajuste de contraste a realizar. Si es 0, se aplica una transformación logarítmica.
                Si es diferente de 0, se aplica una transformación exponencial.
    Retorna:
    numpy.ndarray: La imagen con el contraste ajustado.
    """
    
    img = np.copy(imagen)
    if tipo == 0:
        img = np.clip(np.log1p(contraste * img) / np.log1p(contraste + 1), 0, 1)
    else:
        img = np.clip(np.exp(contraste * (img - 1)), 0, 1)
    return img

# capa de la imagen 
def capaImagen(img, capa):
    """
    Aplica un efecto de atenuación a los canales de color de una imagen, 
    manteniendo el canal especificado sin cambios significativos.
    Parámetros:
    img (numpy.ndarray): Imagen de entrada representada como un arreglo NumPy.
                         Se espera que tenga tres canales (RGB).
    capa (int): Índice del canal que se desea mantener (0 para rojo, 1 para verde, 2 para azul).
    Retorna:
    numpy.ndarray: Imagen modificada con los canales no seleccionados atenuados.
    """

    imgCapa = np.copy(img)
    imgCapa = quitarAtenuacionCanal(imgCapa)
    
    for i in range(3):
        if i != capa:
            imgCapa[:,:,i] = imgCapa[:,:,i] * 0.1

    return imgCapa

# invertir imagen 
def invertirColoresImagen(img):
    """
    Invierte los colores de una imagen.
    Esta función toma una imagen representada como una matriz NumPy y 
    devuelve una nueva imagen donde los colores han sido invertidos. 
    Se asume que los valores de los píxeles están normalizados entre 0 y 1.
    Parámetros:
    img (numpy.ndarray): La imagen de entrada como una matriz NumPy.
    Retorna:
    numpy.ndarray: La imagen con los colores invertidos.
    """
    return 1 - img

# quitar canal de la imagen
def quitarCanal(img, canal):
    """
    Elimina un canal específico de una imagen y devuelve la imagen resultante.
    Parámetros:
    img (numpy.ndarray): La imagen de entrada en formato de matriz numpy con tres canales (RGB).
    canal (int): El índice del canal que se desea eliminar (0 para rojo, 1 para verde, 2 para azul).
    Retorna:
    numpy.ndarray: Una nueva imagen con la misma dimensión que la imagen de entrada, 
                   pero con el canal especificado eliminado.
    """
    imgCanal = np.copy(img)
    imgCanal = quitarAtenuacionCanal(imgCanal)
    imgCanal[:,:,canal] = imgCanal[:,:,canal] * 0.1  # Eliminar el canal especificado
    return imgCanal

# quitar atenuacion de la imagen
def quitarAtenuacionCanal(imagen, factor_recuperacion=10):
    """
    Corrige la atenuación en los canales de color de una imagen.
    Esta función ajusta los valores de los canales de color (R, G, B) de una imagen
    si alguno de ellos está atenuado en comparación con los otros. La corrección
    se realiza multiplicando los valores del canal atenuado por un factor de recuperación.
    Args:
        imagen (numpy.ndarray): Imagen de entrada representada como un arreglo NumPy
            con forma (alto, ancho, 3), donde el último eje corresponde a los canales
            de color (R, G, B).
        factor_recuperacion (float, opcional): Factor por el cual se multiplicará el
            canal atenuado para corregirlo. El valor predeterminado es 10.
    Returns:
        numpy.ndarray: Imagen corregida con los canales atenuados ajustados.
    """
    
    imagen_corregida = imagen.copy()
    
    for canal in range(3):  # Iterar sobre R, G, B
        media_canal = np.mean(imagen[:, :, canal])  # Media del canal actual
        medias_otros = [np.mean(imagen[:, :, i]) for i in range(3) if i != canal]  # Media de los otros dos canales
        media_promedio = np.mean(medias_otros)  # Media global de los otros canales

        # Si el canal está atenuado, aplicamos corrección
        if media_canal < media_promedio:
            imagen_corregida[:, :, canal] = np.clip(imagen[:, :, canal] * factor_recuperacion, 0, 1)
    
    return imagen_corregida

# fusionar imagenes
def fusionar_imagenes(imagen1, imagen2, alpha=0.5, x_offset=0, y_offset=0):
    """
    Fusiona dos imágenes superponiendo una sobre la otra con un nivel de transparencia especificado.
    Args:
        imagen1 (numpy.ndarray): La imagen base sobre la cual se fusionará la segunda imagen.
        imagen2 (numpy.ndarray): La imagen que se superpondrá sobre la imagen base.
        alpha (float, opcional): Nivel de transparencia de la imagen superpuesta. 
                                 Valores entre 0 (completamente transparente) y 1 (completamente opaca). 
                                 Por defecto es 0.5.
        x_offset (int, opcional): Desplazamiento horizontal (en píxeles) desde la esquina superior izquierda 
                                  de la imagen base donde se colocará la imagen superpuesta. Por defecto es 0.
        y_offset (int, opcional): Desplazamiento vertical (en píxeles) desde la esquina superior izquierda 
                                  de la imagen base donde se colocará la imagen superpuesta. Por defecto es 0.
    Returns:
        numpy.ndarray: Una nueva imagen que resulta de la fusión de las dos imágenes.
    Notas:
        - Si la imagen superpuesta (imagen2) excede los límites de la imagen base (imagen1), 
          se recortará automáticamente para ajustarse.
        - La función no modifica las imágenes originales, sino que trabaja con copias.
    Ejemplo:
        resultado = fusionar_imagenes(imagen1, imagen2, alpha=0.7, x_offset=50, y_offset=100)
    """

    # Hacer una copia para no modificar la imagen base original
    resultado = np.copy(imagen1)
    
    # Dimensiones de la marca de agua y de la imagen base
    h1, w1, _ = imagen1.shape
    h2, w2, _ = imagen2.shape
    
    x_fin = min(w1, x_offset + w2)
    y_fin = min(h1, y_offset + h2)
    
    # Se extrae la región de la imagen base donde se colocará la marca de agua.
    roi = resultado[y_offset:y_fin, x_offset:x_fin]
    img2_recorte = imagen2[: (y_fin - y_offset), : (x_fin - x_offset)]
    
    # Procesar según la cantidad de canales
    if img2_recorte.shape[2] == 4:
        # Separa los canales RGB y el canal alfa
        imagen_2_rgb = img2_recorte[:, :, :3]
        imagen_2_alpha = img2_recorte[:, :, 3]
        # Convertir el canal alfa a una máscara 3D y combinarla con el parámetro alpha
        mask = np.expand_dims(imagen_2_alpha, axis=2) * alpha
    else:
        imagen_2_rgb = img2_recorte
        mask = alpha  # se aplica un valor escalar a todos los píxeles
    
    # Se combina la imagen 1 y 2 con la región de la imagen base utilizando la máscara.
    roi_blended = mask * imagen_2_rgb + (1 - mask) * roi
    # Se inserta la imagen procesada en la imagen final.
    resultado[y_offset:y_fin, x_offset:x_fin] = roi_blended
    
    return resultado

# rotar imagen
def rotar_imagen(img, angulo):
    """
    Rota una imagen en un ángulo especificado manteniendo toda la imagen visible,
    usando solo numpy y matplotlib.
    
    Parámetros:
    img (ndarray): Imagen a rotar (matriz numpy).
    angulo (float): Ángulo en grados para rotar la imagen. Los valores positivos rotan la imagen en sentido antihorario.
    
    Retorna:
    ndarray: Imagen rotada con valores de píxeles entre 0 y 1.
    """
    # Si el ángulo es 0 o múltiplo de 360, devolver la imagen original sin cambios
    if angulo % 360 == 0:
        return np.copy(img)
        
    h, w = img.shape[:2]
    angulo_rad = np.radians(angulo)
    
    # Calcular las nuevas dimensiones para contener toda la imagen rotada
    # |cos(ángulo)| * ancho + |sin(ángulo)| * alto
    w_rot = int(abs(np.cos(angulo_rad) * w) + abs(np.sin(angulo_rad) * h))
    h_rot = int(abs(np.sin(angulo_rad) * w) + abs(np.cos(angulo_rad) * h))
    
    # Centro de la imagen original y rotada
    x_centro_orig, y_centro_orig = w / 2, h / 2
    x_centro_rot, y_centro_rot = w_rot / 2, h_rot / 2
    
    # Color de fondo del visor (#606470) convertido a RGB normalizado [0-1]
    # Convertir de hex a RGB [0-1]
    r = int('60', 16) / 255.0
    g = int('64', 16) / 255.0
    b = int('70', 16) / 255.0
    color_fondo = [r, g, b]  # Color de fondo del visor
    
    # Crear nueva imagen más grande para contener toda la rotación con el color de fondo del visor
    img_rotada = np.ones((h_rot, w_rot, img.shape[2]))
    for c in range(img.shape[2]):
        img_rotada[:, :, c] *= color_fondo[c]
    
    # Crear coordenadas para la nueva imagen
    y_rot, x_rot = np.indices((h_rot, w_rot)).astype(np.float64)
    
    # Ajustar coordenadas respecto al centro de la imagen rotada
    x_rot -= x_centro_rot
    y_rot -= y_centro_rot
    
    # Rotar las coordenadas en dirección opuesta
    cos_a, sin_a = np.cos(-angulo_rad), np.sin(-angulo_rad)
    x_orig = cos_a * x_rot - sin_a * y_rot + x_centro_orig
    y_orig = sin_a * x_rot + cos_a * y_rot + y_centro_orig
    
    # Filtrar coordenadas válidas dentro de la imagen original
    valid_coords = (x_orig >= 0) & (x_orig < w-1) & (y_orig >= 0) & (y_orig < h-1)
    
    # Interpolación bilineal
    x0 = np.floor(x_orig).astype(int)
    x1 = x0 + 1
    y0 = np.floor(y_orig).astype(int)
    y1 = y0 + 1
    
    # Limitar a índices válidos
    x0 = np.clip(x0, 0, w-1)
    x1 = np.clip(x1, 0, w-1)
    y0 = np.clip(y0, 0, h-1)
    y1 = np.clip(y1, 0, h-1)
    
    # Pesos para interpolación
    wx = x_orig - x0
    wy = y_orig - y0
    
    # Para cada canal, realizar la interpolación bilineal
    for c in range(img.shape[2]):
        # Interpolación bilineal
        top_left = img[y0, x0, c] * (1-wx) * (1-wy)
        top_right = img[y0, x1, c] * wx * (1-wy)
        bottom_left = img[y1, x0, c] * (1-wx) * wy
        bottom_right = img[y1, x1, c] * wx * wy
        
        # Sumar los cuatro valores ponderados solo para las coordenadas válidas
        img_rotada[valid_coords, c] = (
            top_left[valid_coords] + 
            top_right[valid_coords] + 
            bottom_left[valid_coords] + 
            bottom_right[valid_coords]
        )
    
    return np.clip(img_rotada, 0, 1)

# aplicar zoom
def aplicar_zoom(img, factor, x_centro, y_centro):
    """
    Aplica zoom en una imagen centrado en un punto específico.
    
    Parámetros:
    - img: Imagen como array de NumPy.
    - factor: Factor de zoom (>1 para acercar, <1 para alejar).
    - x_centro: Coordenada X del centro de zoom.
    - y_centro: Coordenada Y del centro de zoom.
    
    Retorna:
    - Imagen escalada con zoom.
    """
    h, w = img.shape[:2]
    nuevo_ancho = int(w / factor)
    nuevo_alto = int(h / factor)
    
    x_inicio = max(0, int(x_centro - nuevo_ancho / 2))
    y_inicio = max(0, int(y_centro - nuevo_alto / 2))
    x_fin = min(w, x_inicio + nuevo_ancho)
    y_fin = min(h, y_inicio + nuevo_alto)
    
    img_zoom = img[y_inicio:y_fin, x_inicio:x_fin]
    img_zoom = cv2.resize(img_zoom, (w, h), interpolation=cv2.INTER_LINEAR)
    
    return img_zoom

# guardar imagen 
def guardar_imagen(ruta, img):
    """
    Guarda una imagen representada como un array de NumPy en la ruta especificada.
    
    Parámetros:
    ruta (str): Ruta completa donde se guardará la imagen, incluyendo el nombre y extensión.
    img (ndarray): Imagen a guardar, representada como un array NumPy.
    
    Retorna:
    None
    """
    plt.imsave(ruta, np.clip(img, 0, 1), cmap="gray")
    
# binarizar imagen
def binarizar_imagen(img, umbral=0.5):
    """
    Convierte una imagen en escala de grises a una imagen binaria (blanco y negro) manteniendo el formato RGB.

    Parámetros:
    img (numpy array): Imagen de entrada con 3 canales (RGB) o en escala de grises.
    umbral (float): Valor del umbral para binarizar (0-1).

    Retorna:
    numpy array: Imagen binarizada con 3 canales (RGB).
    """
    # Convertimos la imagen a escala de grises si es RGB
    if len(img.shape) == 3 and img.shape[2] == 3:
        img_gris = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])  # Convertir a escala de grises
    else:
        img_gris = img  # Ya está en escala de grises

    # Aplicamos binarización: 1 (blanco) si el valor es mayor o igual al umbral, 0 (negro) si es menor
    img_binaria = np.where(img_gris >= umbral, 1, 0)

    # Convertimos la imagen binaria en una imagen con 3 canales (RGB)
    img_binaria_rgb = np.stack([img_binaria] * 3, axis=-1)

    return img_binaria_rgb

# histograma
def histograma_imagen(img, bins=50, alpha=0.5):
    """
    Genera y muestra un histograma para cada canal de color (rojo, verde y azul) de una imagen.
    Parámetros:
    -----------
    img : numpy.ndarray
        Imagen de entrada en formato numpy array. Se espera que tenga tres canales (RGB).
        Si los valores de la imagen están en el rango [0, 1], se escalarán automáticamente a [0, 255].
    bins : int, opcional
        Número de divisiones (bins) para el histograma. Por defecto es 50.
    alpha : float, opcional
        Transparencia de las barras del histograma. Por defecto es 0.5.
    Notas:
    ------
    - La función genera un histograma separado para cada canal de color (rojo, verde y azul).
    - Los histogramas se muestran en una figura con tres subgráficos, uno para cada canal.
    """
    
    # Asegurar que la imagen está en rango 0-255 si es necesario
    if img.max() <= 1.0:
        img = (img * 255).astype(np.uint8)

    colores = ['r', 'g', 'b']
    nombres = ['Canal Rojo', 'Canal Verde', 'Canal Azul']

    # Crear una figura más pequeña y compacta
    fig, axes = plt.subplots(3, 1, figsize=(9, 6))  # Tamaño reducido
    fig.suptitle("Histograma de la imagen", fontsize=10)

    # Generar un histograma separado por cada canal
    for i, ax in enumerate(axes):
        canal = img[..., i].flatten()
        ax.hist(canal, bins=bins, color=colores[i], alpha=alpha)
        ax.set_title(nombres[i], fontsize=9)
        ax.set_xlabel("Intensidad de píxeles", fontsize=8)
        ax.set_ylabel("Frecuencia", fontsize=8)
        ax.set_xlim([0, 255])  # Asegurar que los ejes sean consistentes
        ax.tick_params(axis='both', which='major', labelsize=7)  # Tamaño de las etiquetas de los ejes

    plt.tight_layout()
    
    # Centrar la ventana en la pantalla
    mng = plt.get_current_fig_manager()
    if hasattr(mng, 'window'):
        # Para backends que soportan esta funcionalidad (TkAgg, WXAgg, Qt5Agg)
        try:
            # QT backend
            if hasattr(mng, 'window'):
                geom = mng.window.geometry()
                x, y, dx, dy = geom.getRect()
                mng.window.setGeometry(280, 90, dx, dy)
        except:
            try:
                # TkAgg backend
                mng.window.wm_geometry("+300+300")
            except:
                pass  # Ignorar si no se puede centrar
    
    # Usar block=False para evitar bloquear el bucle de eventos existente
    plt.show(block=False)

# filtro de zonas claras 
def filtrar_zonas_claras_oscuras(img, umbral=0.5, modo="claras", color=[1, 0, 0]):
    """
    Aplica un filtro de color a las zonas claras u oscuras de una imagen.
    
    Parámetros:
    - img (numpy.ndarray): Imagen de entrada en formato NumPy con valores normalizados (0 a 1).
    - umbral (float): Valor entre 0 y 1 para definir la separación entre zonas claras y oscuras.
    - modo (str): "claras" para resaltar zonas claras, "oscuras" para resaltar zonas oscuras.
    - color (list): Color a aplicar en formato RGB normalizado (por defecto rojo [1, 0, 0]).
    
    Retorna:
    - numpy.ndarray: Imagen con las zonas resaltadas.
    """
    # Convertir a escala de grises (luminosidad)
    gris = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])

    # Crear máscara de selección
    if modo == "claras":
        mascara = gris >= umbral  # Zonas claras
    else:
        mascara = gris < umbral  # Zonas oscuras

    # Crear una imagen copia para aplicar el filtro
    img_filtrada = np.copy(img)

    # Aplicar el color solo en las zonas seleccionadas
    for i in range(3):  # Para cada canal R, G, B
        img_filtrada[..., i] = np.where(mascara, color[i], img_filtrada[..., i])

    return img_filtrada

# redimensionar imagen
def redimensionar_imagen(imagen, factor):
    """
    Redimensiona una imagen según el factor especificado usando solo NumPy.
    
    Args:
        imagen (numpy.ndarray): La imagen a redimensionar.
        factor (float): Factor de escala. Valores mayores a 1 amplían la imagen, 
                        valores menores a 1 la reducen.
                        
    Returns:
        numpy.ndarray: La imagen redimensionada.
    """
    if imagen is None:
        return None
        
    # Obtener dimensiones originales
    h, w = imagen.shape[:2]
    
    # Calcular nuevas dimensiones
    new_h, new_w = int(h * factor), int(w * factor)
    
    # Crear coordenadas para la nueva imagen
    y_indices = np.linspace(0, h-1, new_h)
    x_indices = np.linspace(0, w-1, new_w)
    
    # Para interpolación vecino más cercano (más rápida)
    y_indices = np.round(y_indices).astype(int)
    x_indices = np.round(x_indices).astype(int)
    
    # Limitar a los límites de la imagen
    y_indices = np.clip(y_indices, 0, h-1)
    x_indices = np.clip(x_indices, 0, w-1)
    
    # Crear una malla de coordenadas
    coord_y, coord_x = np.meshgrid(y_indices, x_indices, indexing='ij')
    
    # Redimensionar cada canal
    if len(imagen.shape) == 3:
        # Imagen con canales (RGB/RGBA)
        channels = imagen.shape[2]
        resized = np.zeros((new_h, new_w, channels), dtype=imagen.dtype)
        
        for c in range(channels):
            resized[:, :, c] = imagen[coord_y, coord_x, c]
    else:
        # Imagen en escala de grises
        resized = imagen[coord_y, coord_x]
    
    return resized
