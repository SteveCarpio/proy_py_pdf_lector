# model_runner.py
# -------------------------------------------
# Envía el texto de la factura al modelo LLM
# y extrae los campos requeridos como JSON.
# -------------------------------------------

import subprocess
import json
from utils.constants import CAMPOS

def run_model(text, model="mistral"):
    """
    Ejecuta el modelo Mistral (vía Ollama) para procesar el texto y
    devolver un JSON con los campos extraídos.
    """
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
- "Numero_factura" (puede aparecer como: "Nº factura", "Número de factura", "Factura nº", "Expediente")
- "Fecha_emision" (puede aparecer como: "Fecha", "Fecha emisión", "Emisión", "Expedida")
- "Nombre_proveedor" (puede aparecer como: "emisor", "proveedor", "seller", "vendor", "razón social emisor")
- "NIF_CIF_proveedor" (número fiscal del proveedor, puede aparecer como NIF o CIF)
- "Base_imponible" (puede aparecer como: "base", "base imponible", o suele ser la cantidad que resulta de restar el IVA al Total Factura)
- "IVA" (importe del IVA)
- "Total_factura" (puede aparecer como: "Total", "Total a Pagar", "monto total", "total factura")
- "Tipo_fondo" (debe ser exactamente "TDA 22" o "TDA 28")
- "Id_prestamo" (número de 14 dígitos que comienza por 5200015, si contiene "puntos" su tamaño será mayor a 14)
- "Numero_Procd" (puede aparecer como: "Procd")
- "IRPF" (puede aparecer como: "IRPF", "RPF", "LR.P.F"; no es un porcentaje, sino un importe)

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
