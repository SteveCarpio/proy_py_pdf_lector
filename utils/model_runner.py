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
