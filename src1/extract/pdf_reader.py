import pdfplumber
from pdf2image import convert_from_path

def extraer_texto_pdf(path_pdf):
    texto = ""
    con_texto = False

    with pdfplumber.open(path_pdf) as pdf:
        for page in pdf.pages:
            txt = page.extract_text()
            if txt:
                texto += txt + "\n"
                con_texto = True

    return con_texto, texto

def convertir_pdf_a_imagenes(path_pdf):
    return convert_from_path(path_pdf)
