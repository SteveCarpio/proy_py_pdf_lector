import subprocess

def extraer_datos_factura(texto_factura, modelo="mistral"):
    prompt1 = f"""
Eres un sistema inteligente de extracción de datos de facturas. A partir del siguiente texto extraído de una factura, genera un JSON con los siguientes campos:
- Numero_factura
- Fecha_emisión
- Nombre_proveedor
- NIF_CIF_proveedor
- Base_imponible
- IVA
- Total_factura

Además quiero que me crees un campo 'Tipo_fondo', que podrá tener el texto 'TDA 22' o 'TDA 28'
Además en las facturas vienen un valor con 14 dígitos, donde los primeros 7 primeros vienen con el valor: 5200015 ese valor me lo debes crear como un campo 'Id_prestamo'
Texto de la factura:
\"\"\"
{texto_factura}
\"\"\"
"""

    prompt2 = f"""
    Extrae la siguiente información de una factura y responde **solo** con el JSON plano, sin texto adicional. No modificar las comas por el punto en los importes en mi región usamos la coma como separador de decimales

    Campos requeridos:
    - Numero_factura
    - Fecha_emision
    - Nombre_proveedor
    - NIF_CIF_proveedor
    - Base (es la base imponible de la factura)
    - IVA
    - Total_factura (puede venir con la palabra solo 'total')
    - Tipo_fondo (TDA 22 o TDA 28)
    - Id_prestamo (número de 14 dígitos que comienza con 5200015)

    Texto de la factura:
    \"\"\"{texto_factura}\"\"\"
    """

    prompt = f"""
Analiza el texto de una factura y extrae los siguientes campos. 
Responde exclusivamente con un JSON plano, **sin texto adicional**.

Importante:
- Usa coma (",") como separador decimal en los importes, no modificarlo.
- Si no se encuentra algún campo, incluirlo como `null`.
- Los nombres de campos en el JSON deben escribirse tal como se listan a continuación, aunque el texto en la factura use otras expresiones.

Campos requeridos:
- "Numero_factura" → puede aparecer como "Nº factura", "Número de factura", "Factura nº", "Expediente"
- "Fecha_emision" → puede aparecer como "Fecha", "Fecha emisión", "Emisión", "Expedida"
- "Nombre_proveedor" → nombre de la empresa emisora de la factura, suele estar con el texto "S.L"
- "NIF_CIF_proveedor" → número fiscal del proveedor (CIF o NIF)
- "Base_imponible" → puede aparecer como "base", "base imponible" o suele ser una cantidad que es la resta entre IVA y el Total Factura
- "IVA" → importe del IVA
- "Total_factura" → puede aparecer como "Total", "Total a Pagar"
- "Tipo_fondo" → debe ser "TDA 22" o "TDA 28"
- "Id_prestamo" → número de 14 dígitos que comienza por 5200015, si contiene "puntos" su tamaño será mayor a 14
- "Numero_Procd" → puede aparecer como "Procd"
- "IRPF" → puede aparecer como "IRPF", "RPF", "LR.P.F", no es una cantidad que tenga el símbolo de porcentaje

📄 Texto de la factura:
\"\"\"{texto_factura}\"\"\"
"""

    proceso = subprocess.run(
        ['ollama', 'run', modelo],
        input=prompt.encode('utf-8'),
        stdout=subprocess.PIPE
    )
    return proceso.stdout.decode()
