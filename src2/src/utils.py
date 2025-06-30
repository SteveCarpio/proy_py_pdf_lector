import pdfplumber
from pdf2image import convert_from_bytes
import pytesseract
import subprocess
import json
import pandas as pd
from io import BytesIO
import re
from datetime import datetime

CAMPOS = [
    "Número", "Emisor", "CIF Emisor", "Fecha", "Vencimiento",
    "Dirección Emisor", "Correo Emisor", "Nombre Cliente", "Correo Cliente",
    "CIF Cliente", "Base Imponible", "IVA", "Total", "Moneda"
]

def extract_text(file_bytes):
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
            text += pytesseract.image_to_string(img, lang="spa") + "\n"
    return text

def run_model(text, model="mistral"):
    ejemplos = [
        {
            "Número": "INV-2023-045",
            "Emisor": "Servicios Cloud S.A.",
            "CIF Emisor": "B12345678",
            "Fecha": "2023-09-12",
            "Vencimiento": "2023-10-12",
            "Dirección Emisor": "Av. Ejemplo 101, Madrid",
            "Correo Emisor": "info@cloud.com",
            "Nombre Cliente": "Carlos López",
            "Correo Cliente": "carlos@cliente.com",
            "CIF Cliente": "X9988776Q",
            "Base Imponible": "850.00",
            "IVA": "178.50",
            "Total": "1028.50",
            "Moneda": "EUR"
        },
        {
            "Número": "F-001",
            "Emisor": "Papelería Ana",
            "CIF Emisor": "B99988877",
            "Fecha": "2024-01-05",
            "Vencimiento": "2024-01-20",
            "Dirección Emisor": "Calle Mayor 3",
            "Correo Emisor": "ana@papeleria.com",
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
    try:
        return "{:.2f}".format(float(valor))
    except:
        return valor

def limpiar_campos(data):
    campos_num = ["Base Imponible", "IVA", "Total"]
    campos_fecha = ["Fecha", "Vencimiento"]
    for f in campos_num:
        data[f] = normalizar_numero(data.get(f, ""))
    for f in campos_fecha:
        data[f] = normalizar_fecha(data.get(f, ""))
    return data

def valida_campos(d):
    ok = True
    msg = ""

    if not re.match(r"\d{4}-\d{2}-\d{2}", d.get("Fecha", "")):
        ok = False
        msg += "❌ Fecha inválida. "

    for campo in ["Base Imponible", "IVA", "Total"]:
        try:
            float(d[campo])
        except:
            ok = False
            msg += f"❌ '{campo}' no es numérico. "

    return ok, msg

