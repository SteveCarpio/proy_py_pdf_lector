import subprocess

def extraer_datos_factura(texto_factura, modelo="mistral"):
    prompt = f"""
Eres un sistema inteligente de extracción de datos de facturas. A partir del siguiente texto extraído de una factura, genera un JSON con los siguientes campos:
- Número de factura
- Fecha de emisión
- Nombre del proveedor
- NIF/CIF del proveedor
- Base imponible
- IVA
- Total factura

Texto de la factura:
\"\"\"
{texto_factura}
\"\"\"
"""
    proceso = subprocess.run(
        ['ollama', 'run', modelo],
        input=prompt.encode('utf-8'),
        stdout=subprocess.PIPE
    )
    return proceso.stdout.decode()
