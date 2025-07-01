import cv2
import numpy as np
from PIL import Image
import pdfplumber
from pdf2image import convert_from_bytes
import pytesseract
import subprocess
import json
import pandas as pd
from io import BytesIO
import re
from datetime import datetime

CAMPOS_original = [
    "Número", "Emisor", "CIF Emisor", "Fecha", "Vencimiento",
    "Dirección Emisor", "Correo Emisor", "Nombre Cliente", "Correo Cliente",
    "CIF Cliente", "Base Imponible", "IVA", "Total", "Moneda"
]

CAMPOS = [
    "Numero_factura",
    "Fecha_emision",
    "Nombre_proveedor",
    "NIF_CIF_proveedor",
    "Base_imponible",
    "IVA",
    "Total_factura",
    "Tipo_fondo",
    "Id_prestamo",
    "Numero_Procd",
    "IRPF"
]

def preprocess_image(pil_img):
    # Convertir imagen PIL a OpenCV
    img_cv = np.array(pil_img)
    # Convertir a escala de grises
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    # Aplicar umbral adaptativo para mejorar contraste
    thresh = cv2.adaptiveThreshold(gray, 255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    return thresh

def extract_text(file_bytes):
    text = ""
    # 1. Intentar extraer texto directamente (PDF digital)
    try:
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except:
        pass
    
    # 2. Si no hay texto extraído, usar OCR
    if not text.strip():
        images = convert_from_bytes(file_bytes)
        for img in images:
            # Preprocesamiento antes del OCR
            preprocessed = preprocess_image(img)
            ocr_text = pytesseract.image_to_string(preprocessed, lang="spa")
            text += ocr_text + "\n"

    return text

def run_model(text, model="mistral"):
    ejemplos = [
        {
            "Numero_factura": "INV-2023-045",
            "Fecha_emision": "2023-09-12",
            "Nombre_proveedor": "Servicios Cloud S.A.",
            "NIF_CIF_proveedor": "B12345678",
            "Base_imponible": "850,00",
            "IVA": "178,50",
            "Total_factura": "1028,50",
            "Tipo_fondo": "TDA 22",
            "Id_prestamo": "52000151234567",
            "Numero_Procd": "PRC-203",
            "IRPF": "0,00"
        },
        {
            "Numero_factura": "F-001",
            "Fecha_emision": "2024-01-05",
            "Nombre_proveedor": "Papelería Eva",
            "NIF_CIF_proveedor": "B99988877",
            "Base_imponible": "200,00",
            "IVA": "42,00",
            "Total_factura": "242,00",
            "Tipo_fondo": "TDA 28",
            "Id_prestamo": "52000159876543",
            "Numero_Procd": "PRC-119",
            "IRPF": "0,00"
        }
    ]

    ejemplos_json = "\n\n".join(json.dumps(e, ensure_ascii=False) for e in ejemplos)

    prompt = f"""
Analiza el siguiente texto de una factura española y extrae los siguientes campos.  
Responde únicamente con un JSON plano (sin ningún texto antes o después del JSON).

Instrucciones importantes:
- Usa coma (",") como separador decimal en los importes. No modifiques el formato original de los importes ni de la moneda.
- Si algún campo no se encuentra, inclúyelo en el JSON con valor null.
- Los nombres de los campos deben estar entre comillas dobles y escribirse exactamente como aparecen en la lista siguiente, aunque en la factura aparezcan con otras expresiones o en mayúsculas/minúsculas diferentes.
- Si un importe incluye el símbolo de euro (€), mantenlo tal cual.
- Si hay varios valores posibles para un campo, selecciona el primero que aparezca en el texto.
- Devuelve únicamente el JSON, sin explicaciones, comentarios ni texto adicional.

Campos requeridos:
- "Numero_factura"
- "Fecha_emision"
- "Nombre_proveedor"
- "NIF_CIF_proveedor"
- "Base_imponible"
- "IVA"
- "Total_factura"
- "Tipo_fondo"
- "Id_prestamo"
- "Numero_Procd"
- "IRPF"

Ejemplos de salida esperada:

{ejemplos_json}

📄 Texto de la factura:
\"\"\"{text}\"\"\"
    """.strip()

    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode("utf-8"),
        capture_output=True
    )
    output = result.stdout.decode("utf-8")

    try:
        parsed_json = json.loads(output[output.find("{"):output.rfind("}")+1])
    except:
        parsed_json = {}

    return {campo: parsed_json.get(campo, "") for campo in CAMPOS}



def run_model_original(text, model="mistral"):
    ejemplos = [
        {
            "Número": "INV-2023-045",
            "Emisor": "Servicios Cloud S.A.",
            "CIF Emisor": "B12345678",
            "Fecha": "2023-09-12",
            "Vencimiento": "2023-10-12",
            "Dirección Emisor": "Av. Ejemplo 101, Madrid",
            "Correo Emisor": "info@cloud.com",
            "Nombre Cliente": "Steve Carpio",
            "Correo Cliente": "stv.madrid@gmail.com",
            "CIF Cliente": "X9988776Q",
            "Base Imponible": "850.00",
            "IVA": "178.50",
            "Total": "1028.50",
            "Moneda": "EUR"
        },
        {
            "Número": "F-001",
            "Emisor": "Papelería Eva",
            "CIF Emisor": "B99988877",
            "Fecha": "2024-01-05",
            "Vencimiento": "2024-01-20",
            "Dirección Emisor": "Calle Mayor 3",
            "Correo Emisor": "eva@papeleria.com",
            "Nombre Cliente": "Empresa Beta",
            "Correo Cliente": "contacto@empresa.com",
            "CIF Cliente": "B11223344",
            "Base Imponible": "200.00",
            "IVA": "42.00",
            "Total": "242.00",
            "Moneda": "EUR"
        }
    ]

    ejemplos_json = "\n\n".join(json.dumps(e, ensure_ascii=False) for e in ejemplos)

    prompt = f"""
Extrae los datos de una factura en español. Devuelve un JSON siguiendo estos ejemplos:

{ejemplos_json}

A continuación el texto a procesar:
{text}
    """.strip()

    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode("utf-8"),
        capture_output=True
    )
    output = result.stdout.decode("utf-8")

    try:
        parsed_json = json.loads(output[output.find("{"):output.rfind("}")+1])
    except:
        parsed_json = {}

    return {campo: parsed_json.get(campo, "") for campo in CAMPOS}

def normalizar_fecha(fecha):
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d", "%Y-%m-%d"):
        try:
            return datetime.strptime(fecha.strip(), fmt).strftime("%Y-%m-%d")
        except:
            continue
    return fecha

def normalizar_numero(valor):
    valor = valor.replace("€", "").strip()
    valor = valor.replace(",", ".")
    valor = valor.replace(",", ".")
    try:
        return "{:.2f}".format(float(valor))
    except:
        return valor

def limpiar_campos(data):
    campos_num = ["Base_imponible", "IVA", "Total_factura"]
    campos_fecha = ["Fecha_emision"]  # campos_fecha = ["Fecha_emision", "Vencimiento"]
    for f in campos_num:
        data[f] = normalizar_numero(data.get(f, ""))
    for f in campos_fecha:
        data[f] = normalizar_fecha(data.get(f, ""))
    return data

def valida_campos(d):
    ok = True
    msg = ""

    if not re.match(r"\d{4}-\d{2}-\d{2}", d.get("Fecha_emision", "")):
        ok = False
        msg += "❌ Fecha inválida. "

    for campo in ["Base_imponible", "IVA", "Total_factura"]:
        try:
            float(d[campo])
        except:
            ok = False
            msg += f"❌ '{campo}' no es numérico. "

    return ok, msg

