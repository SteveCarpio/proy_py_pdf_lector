# ocr_utils.py
# -------------------------------------------
# Funciones para preprocesar imágenes y extraer 
# texto de PDFs usando OCR (Tesseract) o pdfplumber.
# -------------------------------------------

import cv2
import numpy as np
from PIL import Image
import pdfplumber
from pdf2image import convert_from_bytes
import pytesseract
from io import BytesIO

def preprocess_image(pil_img):
    """
    Preprocesa una imagen PIL para mejorar la legibilidad del OCR.
    Convierte a escala de grises y aplica umbral adaptativo.
    """
    img_cv = np.array(pil_img)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        11, 2
    )
    return thresh

def extract_text(file_bytes):
    """
    Extrae texto de un archivo PDF:
    - Si es digital, usa pdfplumber.
    - Si es escaneado, aplica OCR con Tesseract.
    """
    text = ""

    try:
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except:
        pass

    if not text.strip():
        images = convert_from_bytes(file_bytes)
        for img in images:
            preprocessed = preprocess_image(img)
            ocr_text = pytesseract.image_to_string(preprocessed, lang="spa")
            text += ocr_text + "\n"

    return text
