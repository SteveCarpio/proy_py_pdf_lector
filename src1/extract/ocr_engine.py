import pytesseract
import cv2
import numpy as np

def imagen_a_texto(pil_image):
    imagen_cv = np.array(pil_image)
    imagen_gray = cv2.cvtColor(imagen_cv, cv2.COLOR_BGR2GRAY)
    texto = pytesseract.image_to_string(imagen_gray, lang='spa')
    return texto
