import os
from pdf2image import convert_from_path
from PIL import Image
import numpy as np
import cv2
import pytesseract

def preprocess_image(pil_img):
    """
    Convierte la imagen PIL a OpenCV, escala de grises,
    y aplica umbral adaptativo para mejorar OCR.
    """
    img_cv = np.array(pil_img)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    return thresh

def validar_y_ocr_pdf(pdf_path, carpeta_salida, archivo_texto_ocr=None):
    """
    Procesa un PDF: convierte cada página en imagen, la guarda,
    hace OCR con Tesseract y guarda todo el texto.
    """
    if not os.path.exists(carpeta_salida):
        os.makedirs(carpeta_salida)

    print(f"📄 Procesando PDF: {pdf_path}")
    pages = convert_from_path(pdf_path, dpi=300)

    ocr_resultado = []

    for i, page in enumerate(pages):
        # 1. Preprocesar imagen
        preprocessed = preprocess_image(page)

        # 2. Guardar imagen para validación visual
        nombre_img = os.path.join(carpeta_salida, f"pagina_{i+1:03}.png")
        cv2.imwrite(nombre_img, preprocessed)
        print(f"🖼️ Imagen guardada: {nombre_img}")

        # 3. OCR en la imagen preprocesada
        ocr_text = pytesseract.image_to_string(preprocessed, lang="spa")
        ocr_resultado.append(f"--- Página {i+1} ---\n{ocr_text.strip()}\n")

    # 4. Guardar el texto OCR si se solicita
    if archivo_texto_ocr:
        with open(archivo_texto_ocr, "w", encoding="utf-8") as f:
            f.write("\n\n".join(ocr_resultado))
        print(f"\n📝 OCR guardado en: {archivo_texto_ocr}")

    print("\n✅ OCR terminado. Puedes revisar las imágenes y el texto extraído.")



# ⚙️ Configura tus rutas aquí
pdf_entrada = r"H:\Proyectos\Python\x2\x\F00882-25 MONTERO PR PF 4123 YA PAGADA 042025.pdf"
carpeta_imagenes = r"C:\Users\scarpio\Documents\GitHub\proy_py_pdf_lector\img"
archivo_resultado_txt = r"C:\Users\scarpio\Documents\GitHub\proy_py_pdf_lector\img\resultado_ocr.txt"

validar_y_ocr_pdf(pdf_entrada, carpeta_imagenes, archivo_resultado_txt)



