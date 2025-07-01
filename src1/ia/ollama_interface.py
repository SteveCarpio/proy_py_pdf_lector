import subprocess

def extraer_datos_factura(texto_factura, modelo="llama3"): # llama3 / mistral

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

📄 Texto de la factura:
\"\"\"{texto_factura}\"\"\"
"""


    proceso = subprocess.run(
        ['ollama', 'run', modelo],
        input=prompt.encode('utf-8'),
        stdout=subprocess.PIPE
    )
    return proceso.stdout.decode()
