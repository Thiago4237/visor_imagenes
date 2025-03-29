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
        img = np.clip(np.log1p(contraste * img) / np.log1p(contraste), 0, 1)
    else:
        img = np.clip(np.exp(contraste * (img - 1)), 0, 1)
    return img

# capa de la imagen 
def capaImagen(img, capa):
    """
    Extrae una capa específica de una imagen y la devuelve como una nueva imagen con tres canales.
    Parámetros:
    img (numpy.ndarray): La imagen de entrada en formato de matriz numpy con tres canales (RGB).
    capa (int): El índice de la capa que se desea extraer (0 para rojo, 1 para verde, 2 para azul).
    Retorna:
    numpy.ndarray: Una nueva imagen con la misma dimensión que la imagen de entrada, 
                   pero con todos los canales en cero excepto la capa especificada.
    """
    fila,columna = img.shape[:2]
    imgCapa = np.zeros((fila,columna,3))
    imgCapa[:,:,capa] = img[:,:,capa]
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
    imgCanal[:,:,canal] = 0
    return imgCanal

# marca de agua
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
    
    # Se inserta la imagen procesada en la imagen final.
    resultado[y_offset:y_fin, x_offset:x_fin] = alpha * img2_recorte + (1 - alpha) * roi
    
    return resultado

# rotar imagen
def rotar_imagen(img, angulo):
    """
    Rota una imagen en un ángulo especificado usando solo numpy y matplotlib.
    
    Parámetros:
    img (ndarray): Imagen a rotar (matriz numpy).
    angulo (float): Ángulo en grados para rotar la imagen. Los valores positivos rotan la imagen en sentido antihorario.
    
    Retorna:
    ndarray: Imagen rotada con valores de píxeles entre 0 y 1.
    """
    angulo_rad = np.radians(angulo)
    h, w = img.shape[:2]
    y, x = np.indices((h, w))
    
    # Centro de la imagen
    x_centro, y_centro = w / 2, h / 2
    
    x = x.astype(np.float64)  # Convertir a float64 antes de la resta
    y = y.astype(np.float64)
    
    x -= x_centro
    y -= y_centro

    # Rotación de coordenadas
    cos_a, sin_a = np.cos(angulo_rad), np.sin(angulo_rad)
    x_rot = cos_a * x - sin_a * y + x_centro
    y_rot = sin_a * x + cos_a * y + y_centro

    # Redondeo a índices válidos dentro de la imagen
    x_rot = np.clip(x_rot, 0, w - 1)
    y_rot = np.clip(y_rot, 0, h - 1)

    # Interpolación bilineal manual
    x0 = np.floor(x_rot).astype(int)
    x1 = np.clip(x0 + 1, 0, w - 1)
    y0 = np.floor(y_rot).astype(int)
    y1 = np.clip(y0 + 1, 0, h - 1)

    # Pesos de interpolación
    wa = (x1 - x_rot) * (y1 - y_rot)
    wb = (x_rot - x0) * (y1 - y_rot)
    wc = (x1 - x_rot) * (y_rot - y0)
    wd = (x_rot - x0) * (y_rot - y0)

    # Aplicar interpolación a cada canal
    img_rotada = np.zeros_like(img)
    for c in range(img.shape[2]):
        img_rotada[:, :, c] = (
            wa * img[y0, x0, c] +
            wb * img[y0, x1, c] +
            wc * img[y1, x0, c] +
            wd * img[y1, x1, c]
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
    Convierte una imagen en escala de grises a una imagen binaria (blanco y negro).

    Parámetros:
    img (numpy array): Imagen en escala de grises.
    umbral (int): Valor de umbral para binarizar (0-1).

    Retorna:
    numpy array: Imagen binarizada (solo 0 y 1).
    """
    # Convertimos la imagen a escala de grises si no lo está
    if len(img.shape) == 3:  # Si la imagen tiene 3 canales (RGB)
        img = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])  # Conversión a escala de grises

    # Aplicamos binarización: Si el valor es mayor o igual al umbral → 1 (blanco), sino → 0 (negro)
    img_binaria = np.where(img >= umbral, 1, 0)

    return img_binaria

# histograma
def histograma_imagen(img, bins=50, color='r', alpha=0.5, ax=None):
    """
    Genera y muestra un histograma de una imagen dada.
    
    Parámetros:
    img (ndarray): Imagen en formato de matriz numpy.
    bins (int): Número de divisiones en el histograma (por defecto 50).
    color (str): Color de las barras del histograma (por defecto 'r' - rojo).
    alpha (float): Transparencia de las barras (por defecto 0.5).
    ax (matplotlib.axes._subplots.AxesSubplot, opcional): 
        Eje donde se dibujará el histograma. Si es None, se crea una nueva figura.
    
    Retorna:
    None
    """
    img_flatten = img.flatten()  # Aplanar la imagen a un array 1D

    # Si no se proporciona un eje, crear uno nuevo
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 4))
    
    ax.hist(img_flatten, bins=bins, facecolor=color, alpha=alpha)
    ax.set_title("Histograma de la Imagen")
    ax.set_xlabel("Intensidad de píxeles")
    ax.set_ylabel("Frecuencia")

    # Mostrar la figura solo si no se usó un eje externo
    if ax is None:
        plt.show()


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
